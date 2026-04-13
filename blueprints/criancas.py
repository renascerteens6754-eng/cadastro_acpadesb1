from flask import Blueprint, request, jsonify
from db_config import connect_db
from datetime import datetime, date
import traceback

criancas_bp = Blueprint("criancas", __name__, url_prefix="/criancas")


@criancas_bp.route("/", methods=["GET"])
def listar():
    try:
        supabase = connect_db()
        resp = supabase.table("criancas").select("*").order("nome").execute()
        return jsonify(resp.data or []), 200
    except Exception as e:
        print("ERRO LISTAR:", str(e))
        return jsonify([]), 200


@criancas_bp.route("/", methods=["POST"])
def cadastrar():
    try:
        supabase = connect_db()
        data = request.json
        result = supabase.table("criancas").insert(data).execute()
        return jsonify(result.data[0]), 201
    except Exception as e:
        print("ERRO CADASTRAR:", str(e))
        return jsonify({"erro": str(e)}), 500


@criancas_bp.route("/<int:id>", methods=["PUT"])
def atualizar(id):
    try:
        supabase = connect_db()
        data = request.json
        resp = supabase.table("criancas").update(data).eq("id", id).execute()
        return jsonify(resp.data[0]), 200
    except Exception as e:
        print("ERRO ATUALIZAR:", str(e))
        return jsonify({"erro": str(e)}), 500


@criancas_bp.route("/<int:id>", methods=["DELETE"])
def deletar(id):
    try:
        supabase = connect_db()
        supabase.table("criancas").delete().eq("id", id).execute()
        return jsonify({"ok": True}), 200
    except Exception as e:
        print("ERRO DELETAR:", str(e))
        return jsonify({"erro": str(e)}), 500


@criancas_bp.route("/migrar-para-adolescentes", methods=["POST"])
def migrar_para_adolescentes():
    try:
        supabase = connect_db()
        resp = supabase.table("criancas").select("*").execute()
        criancas = resp.data or []

        hoje = date.today()
        migradas = []

        for crianca in criancas:
            data_nasc_str = crianca.get("data_nasc")
            if not data_nasc_str:
                continue

            data_nasc = datetime.strptime(data_nasc_str, "%Y-%m-%d").date()
            idade = hoje.year - data_nasc.year
            if hoje.month < data_nasc.month or (hoje.month == data_nasc.month and hoje.day < data_nasc.day):
                idade -= 1

            if idade >= 12:
                dados_adolescente = {
                    "nome": crianca.get("nome"),
                    "nome_pai": crianca.get("nome_pai"),
                    "nome_mae": crianca.get("nome_mae"),
                    "cpf": crianca.get("cpf"),
                    "rg": crianca.get("rg"),
                    "contato": crianca.get("contato"),
                    "data_nasc": crianca.get("data_nasc"),
                    "congregacao": crianca.get("congregacao"),
                    "endereco": crianca.get("endereco")
                }

                insert_result = supabase.table("adolescentes").insert(dados_adolescente).execute()

                if insert_result.data:
                    supabase.table("criancas").delete().eq("id", crianca.get("id")).execute()
                    migradas.append({
                        "id_original": crianca.get("id"),
                        "nome": crianca.get("nome"),
                        "idade": idade
                    })

        return jsonify({
            "status": "ok",
            "mensagem": f"{len(migradas)} criança(s) migrada(s)",
            "migradas": migradas
        }), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({"status": "erro", "erro": str(e)}), 500