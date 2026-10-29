import argparse, json, time
from collections import deque

NAMA = {"fill_a":"Isi A","fill_b":"Isi B","empty_a":"Kosongkan A",
        "empty_b":"Kosongkan B","pour_a_b":"Tuang A->B","pour_b_a":"Tuang B->A"}

def successors(s, cfg):
    x, y = s; A, B = cfg["cap_a"], cfg["cap_b"]; out = []
    for op in cfg["operators"]:
        if op == "fill_a": n = (A, y)
        elif op == "fill_b": n = (x, B)
        elif op == "empty_a": n = (0, y)
        elif op == "empty_b": n = (x, 0)
        elif op == "pour_a_b": t = min(x, B - y); n = (x - t, y + t)
        elif op == "pour_b_a": t = min(y, A - x); n = (x + t, y - t)
        else: raise ValueError(f"Operator tidak dikenal: {op}")
        if n != s: out.append((op, n))
    return out

def is_goal(s, cfg): return cfg["target"] in s

def validate_config(cfg):
    if not isinstance(cfg["cap_a"], int) or cfg["cap_a"] <= 0:
        raise ValueError("Kapasitas A harus bilangan bulat positif.")

    if not isinstance(cfg["cap_b"], int) or cfg["cap_b"] <= 0:
        raise ValueError("Kapasitas B harus bilangan bulat positif.")

    if not isinstance(cfg["target"], int) or cfg["target"] < 0:
        raise ValueError("Target harus bilangan bulat nonnegatif.")

    if not isinstance(cfg["start"], list) or len(cfg["start"]) != 2:
        raise ValueError("start harus berupa dua nilai [x, y].")

    x, y = cfg["start"]

    if not isinstance(x, int) or not isinstance(y, int):
        raise ValueError("Volume awal harus berupa bilangan bulat.")

    if not (0 <= x <= cfg["cap_a"] and 0 <= y <= cfg["cap_b"]):
        raise ValueError("Volume awal melebihi kapasitas galon.")

    if cfg["target"] > max(cfg["cap_a"], cfg["cap_b"]):
        raise ValueError("Target melebihi kapasitas kedua galon.")

    if not isinstance(cfg["operators"], list):
        raise ValueError("operators harus berupa daftar.")

    for op in cfg["operators"]:
        if op not in NAMA:
            raise ValueError(f"Operator tidak dikenal: {op}")

def search(cfg, algo, trace=False):
    start = tuple(cfg["start"])
    frontier = deque([start])
    parent = {start: None}
    expanded = 0
    max_frontier = 1

    while frontier:
        s = frontier.popleft() if algo == "bfs" else frontier.pop()

        if is_goal(s, cfg):
            path = []
            cur = s

            while parent[cur] is not None:
                prev, op = parent[cur]
                path.append((op, cur))
                cur = prev

            path.reverse()
            return [(None, start)] + path, expanded, max_frontier

        expanded += 1

        if trace:
            print(f"Expand: {s}")
            print(f"Frontier sebelum successor: {list(frontier)}")

        succ = successors(s, cfg)

        if algo == "dfs":
            succ = succ[::-1]

        for op, n in succ:
            if n in parent:
                continue

            parent[n] = (s, op)
            frontier.append(n)

        max_frontier = max(max_frontier, len(frontier))

        if trace:
            print(f"Frontier sesudah successor: {list(frontier)}")
            print("-" * 40)

    return None, expanded, max_frontier

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--algo", choices=["bfs","dfs"], required=True)
    ap.add_argument("--trace", action="store_true")
    a = ap.parse_args()
    
    try:
        cfg = json.load(open(a.input))

        for k in ("cap_a", "cap_b", "target", "start", "operators"):
            cfg[k]

        validate_config(cfg)

    except (OSError, json.JSONDecodeError, KeyError, ValueError) as e:
        raise SystemExit(f"Error input: {e!r}")

    t0 = time.perf_counter()
    path, exp, mf = search(cfg, a.algo, a.trace)
    dt = (time.perf_counter() - t0) * 1000
    print(f"== {a.algo.upper()} | A={cfg['cap_a']} B={cfg['cap_b']} target={cfg['target']} ==")
    if path is None: print("Tidak ada solusi.")
    else:
        for i, (op, s) in enumerate(path):
            print(f"{i:>2}. {NAMA.get(op,'Awal'):<12} -> {s}")
        print(f"Jumlah langkah   : {len(path)-1}")
    print(f"Node expanded    : {exp}\nFrontier terbesar: {mf}\nWaktu           : {dt:.4f} ms")
main()