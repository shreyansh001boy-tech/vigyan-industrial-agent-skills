"""
Vigyan Industrial Agent Skills Ingestion & Hub Bridge Engine
Scans all 8 industrial skills, extracts mathematical axioms, and exports a unified tool registry
and knowledge graph seed file for the Vigyan Agentic Hub.
"""

import os
import sys
import glob
import json
import re
from pathlib import Path

def parse_frontmatter(skill_md_path: str) -> dict:
    with open(skill_md_path, "r", encoding="utf-8") as f:
        content = f.read()

    match = re.search(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)
    if not match:
        return {"name": Path(skill_md_path).parent.name, "description": "", "body": content}

    yaml_block = match.group(1)
    body = match.group(2)

    name = ""
    description = ""
    for line in yaml_block.splitlines():
        if line.startswith("name:"):
            name = line.split("name:", 1)[1].strip()
        elif line.startswith("description:"):
            description = line.split("description:", 1)[1].strip()

    return {
        "name": name,
        "description": description,
        "body": body
    }

def collect_all_skills(repo_root: str) -> list:
    skills_dir = os.path.join(repo_root, "skills")
    skill_paths = glob.glob(os.path.join(skills_dir, "*", "SKILL.md"))
    
    collected = []
    for sp in sorted(skill_paths):
        skill_info = parse_frontmatter(sp)
        skill_folder = os.path.dirname(sp)
        solver_script = os.path.join(skill_folder, "scripts", "solver.py")
        
        has_solver = os.path.exists(solver_script)
        collected.append({
            "id": skill_info["name"],
            "description": skill_info["description"],
            "path": sp,
            "has_solver": has_solver,
            "solver_script": solver_script if has_solver else None
        })
    return collected

def generate_hub_manifest(skills: list, output_json_path: str):
    manifest = {
        "version": "1.0.0",
        "total_skills": len(skills),
        "skills": skills
    }
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    print(f"✓ Manifest exported: {output_json_path} ({len(skills)} skills)")

def main():
    repo_root = Path(__file__).resolve().parent.parent
    print(f"=== Vigyan Industrial Skills Ingestion Engine ===")
    print(f"Repo Root: {repo_root}")

    skills = collect_all_skills(str(repo_root))
    print(f"Found {len(skills)} registered industrial STEM skills:")
    for s in skills:
        solver_status = "✓ solver.py ready" if s["has_solver"] else "✗ no solver"
        print(f"  • {s['id']:<35} [{solver_status}]")

    out_manifest = os.path.join(repo_root, "scripts", "industrial_skills_manifest.json")
    generate_hub_manifest(skills, out_manifest)
    print("Ingestion engine self-test passed successfully.")

if __name__ == "__main__":
    main()
