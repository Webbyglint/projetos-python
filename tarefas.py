#!/usr/bin/env python3
"""Gerenciador de tarefas via linha de comando, com persistência em JSON."""
import argparse
import json
from datetime import datetime
from pathlib import Path

ARQUIVO = Path("tarefas.json")


def carregar() -> list[dict]:
    if not ARQUIVO.exists():
        return []
    return json.loads(ARQUIVO.read_text(encoding="utf-8"))


def salvar(tarefas: list[dict]) -> None:
    ARQUIVO.write_text(
        json.dumps(tarefas, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def adicionar(descricao: str) -> None:
    tarefas = carregar()
    novo_id = max((t["id"] for t in tarefas), default=0) + 1
    tarefas.append({
        "id": novo_id,
        "descricao": descricao,
        "concluida": False,
        "criada_em": datetime.now().isoformat(timespec="seconds"),
    })
    salvar(tarefas)
    print(f"Tarefa #{novo_id} adicionada.")


def listar(somente_pendentes: bool = False) -> None:
    tarefas = carregar()
    if somente_pendentes:
        tarefas = [t for t in tarefas if not t["concluida"]]
    if not tarefas:
        print("Nenhuma tarefa encontrada.")
        return
    for t in tarefas:
        marca = "x" if t["concluida"] else " "
        print(f"[{marca}] #{t['id']:<3} {t['descricao']}")


def concluir(id_tarefa: int) -> None:
    tarefas = carregar()
    for t in tarefas:
        if t["id"] == id_tarefa:
            t["concluida"] = True
            salvar(tarefas)
            print(f"Tarefa #{id_tarefa} concluída.")
            return
    print(f"Tarefa #{id_tarefa} não encontrada.")


def remover(id_tarefa: int) -> None:
    tarefas = carregar()
    restantes = [t for t in tarefas if t["id"] != id_tarefa]
    if len(restantes) == len(tarefas):
        print(f"Tarefa #{id_tarefa} não encontrada.")
        return
    salvar(restantes)
    print(f"Tarefa #{id_tarefa} removida.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Gerenciador de tarefas")
    sub = parser.add_subparsers(dest="comando", required=True)

    p_add = sub.add_parser("add", help="adiciona uma tarefa")
    p_add.add_argument("descricao")

    p_list = sub.add_parser("list", help="lista tarefas")
    p_list.add_argument("--pendentes", action="store_true")

    p_done = sub.add_parser("done", help="conclui uma tarefa")
    p_done.add_argument("id", type=int)

    p_rm = sub.add_parser("rm", help="remove uma tarefa")
    p_rm.add_argument("id", type=int)

    args = parser.parse_args()
    if args.comando == "add":
        adicionar(args.descricao)
    elif args.comando == "list":
        listar(args.pendentes)
    elif args.comando == "done":
        concluir(args.id)
    elif args.comando == "rm":
        remover(args.id)


if __name__ == "__main__":
    main()
