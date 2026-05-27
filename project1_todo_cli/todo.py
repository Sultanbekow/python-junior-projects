#!/usr/bin/env python3
import json, os, sys
from datetime import datetime

DATA_FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

def add_task(description):
    tasks = load_tasks()
    new_id = max([t["id"] for t in tasks], default=0) + 1
    tasks.append({
        "id": new_id,
        "description": description,
        "completed": False,
        "created_at": datetime.now().isoformat()
    })
    save_tasks(tasks)
    print(f"✅ Aufgabe {new_id} hinzugefügt: {description}")

def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("📭 Keine Aufgaben vorhanden.")
        return
    for t in tasks:
        status = "✅" if t["completed"] else "⏳"
        print(f"{status} [{t['id']}] {t['description']}")

def complete_task(task_id):
    tasks = load_tasks()
    for t in tasks:
        if t["id"] == task_id:
            t["completed"] = True
            save_tasks(tasks)
            print(f"🎉 Aufgabe {task_id} erledigt.")
            return
    print(f"❌ ID {task_id} nicht gefunden.")

def delete_task(task_id):
    tasks = load_tasks()
    new_tasks = [t for t in tasks if t["id"] != task_id]
    if len(new_tasks) == len(tasks):
        print(f"❌ ID {task_id} nicht gefunden.")
    else:
        save_tasks(new_tasks)
        print(f"🗑️ Aufgabe {task_id} gelöscht.")

def print_help():
    print("""
Befehle:
  add <text>   – Aufgabe hinzufügen
  list         – Alle anzeigen
  done <ID>    – Erledigt markieren
  delete <ID>  – Löschen
  help         – Diese Hilfe
  exit         – Beenden
""")

def main():
    print("📋 To-Do CLI. 'help' für Hilfe.")
    while True:
        try:
            cmd = input("\ntodo> ").strip().split()
            if not cmd: continue
            action = cmd[0].lower()
            if action == "add" and len(cmd) > 1:
                add_task(" ".join(cmd[1:]))
            elif action == "list":
                list_tasks()
            elif action == "done" and len(cmd) == 2:
                complete_task(int(cmd[1]))
            elif action == "delete" and len(cmd) == 2:
                delete_task(int(cmd[1]))
            elif action == "help":
                print_help()
            elif action == "exit":
                print("👋 Tschüss!")
                break
            else:
                print("❌ Unbekannt. 'help' zeigt Befehle.")
        except KeyboardInterrupt:
            print("\n👋 Abbruch.")
            break
        except ValueError:
            print("❌ ID muss eine Zahl sein.")

if __name__ == "__main__":
    main()
