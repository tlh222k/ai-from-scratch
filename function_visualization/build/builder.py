"""Build có cache, bảo toàn HTML cũ và cập nhật index."""
from pathlib import Path
import hashlib, json
from .registry import GRAPH_REGISTRY
from function_visualization.core.index import generate_index

PACKAGE_DIR = Path(__file__).resolve().parents[1]
PROJECT_ROOT = PACKAGE_DIR.parent
OUTPUT_DIR = PROJECT_ROOT / "visualizations"
MANIFEST_PATH = Path(__file__).with_name("manifest.json")

def _sha(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def _load_manifest():
    if MANIFEST_PATH.exists():
        try: return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError: pass
    return {"graphs": {}}

def build_all(force=False):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    manifest = _load_manifest()
    records = manifest.setdefault("graphs", {})
    results = {}
    for spec in GRAPH_REGISTRY:
        module = __import__(spec.module, fromlist=["build"])
        source_path = Path(module.__file__)
        output_path = OUTPUT_DIR / spec.output_filename
        source_hash = _sha(source_path)
        old = records.get(spec.graph_id, {})
        if spec.graph_id == "minimum_point":
            if output_path.exists():
                status, reason = "PRESERVED", "Giữ nguyên HTML đã cung cấp; chưa có notebook nguồn để dựng lại."
            else:
                status, reason = "MISSING", "Thiếu HTML điểm cực tiểu."
        elif output_path.exists() and not force and old.get("source_sha256") == source_hash:
            status, reason = "SKIP", "Mã nguồn không đổi; giữ nguyên HTML."
        elif output_path.exists() and not force and not old:
            status, reason = "ADOPT", "Đã nhận diện HTML cũ; không ghi đè trong lần chạy đầu."
        else:
            temp_dir = OUTPUT_DIR / ".build_tmp"
            temp_dir.mkdir(exist_ok=True)
            try:
                generated = module.build(temp_dir)
                generated = Path(generated)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                generated.replace(output_path)
                status, reason = "BUILT", "Đã dựng lại từ module Python."
            finally:
                if temp_dir.exists():
                    for item in temp_dir.iterdir():
                        if item.is_file(): item.unlink()
                    temp_dir.rmdir()
        if output_path.exists():
            records[spec.graph_id] = {"filename": spec.output_filename, "source_sha256": source_hash,
                                      "html_sha256": _sha(output_path), "status": status}
        results[spec.graph_id] = {"status": status, "reason": reason, "path": str(output_path)}
    index_path = generate_index(OUTPUT_DIR)
    manifest["index"] = {"filename": "index.html", "sha256": _sha(index_path)}
    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return results

if __name__ == "__main__":
    for graph_id, result in build_all().items():
        print(f"{graph_id}: {result['status']} — {result['reason']}")
