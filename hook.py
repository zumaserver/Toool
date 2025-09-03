import builtins
import functools
import sys
import os

def main():
    target_file = input("Nhập file cần hook: ").strip()
    if not os.path.exists(target_file):
        print("File không tồn tại.")
        return

    # giữ bản gốc exec
    _orig_exec = builtins.exec

    @functools.wraps(_orig_exec)  # giữ metadata exec để khó phát hiện
    def exec_hook(code, globals=None, locals=None):
        # dump code ra log nhưng vẫn cho chạy
        try:
            if isinstance(code, str):
                dump = code
            elif isinstance(code, (bytes, bytearray)):
                dump = code.decode("utf-8", errors="replace")
            else:
                dump = f"[Non-str exec: {type(code)}]"

            with open("exec_log.txt", "a", encoding="utf-8") as f:
                f.write("\n" + "#" * 40 + "\n")
                f.write(dump + "\n")
                f.write("#" * 40 + "\n")

        except Exception as e:
            print(f"[HOOK WARN] Dump lỗi: {e}")

        # vẫn chạy như bình thường
        return _orig_exec(code, globals, locals)

    # gán hook
    builtins.exec = exec_hook

    # chạy file target
    sys.argv = [target_file]  # giả lập argv
    with open(target_file, "r", encoding="utf-8", errors="ignore") as f:
        source = f.read()
    code_obj = compile(source, target_file, "exec")
    exec(code_obj, {"__name__": "__main__", "__file__": target_file})

    print("\n--- Hoàn tất, payload đã dump ra exec_log.txt ---")

if __name__ == "__main__":
    main()