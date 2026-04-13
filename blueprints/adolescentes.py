from flask import Blueprint, request, jsonify
from db_config import connect_db
import traceback

adolescentes_bp = Blueprint("adolescentes", __name__, url_prefix="/adolescentes")

@adolescentes_bp.route("/", methods=["GET"])
def listar():
    try:
        supabase = connect_db()
        resp = supabase.table("adolescentes").select("*").order("nome").execute()
        return jsonify(resp.data or []), 200
    except Exception as e:
        print("ERRO LISTAR:", str(e))
        return jsonify([]), 200

@adolescentes_bp.route("/", methods=["POST"])
def cadastrar():
    try:
        supabase = connect_db()
        data = request.json
        result = supabase.table("adolescentes").insert(data).execute()
        return jsonify(result.data[0]), 201
    except Exception as e:
        print("ERRO CADASTRAR:", str(e))
        return jsonify({"erro": str(e)}), 500

@adolescentes_bp.route("/<int:id>", methods=["PUT"])
def atualizar(id):
    try:
        supabase = connect_db()
        data = request.json
        resp = supabase.table("adolescentes").update(data).eq("id", id).execute()
        return jsonify(resp.data[0]), 200
    except Exception as e:
        print("ERRO ATUALIZAR:", str(e))
        return jsonify({"erro": str(e)}), 500

@adolescentes_bp.route("/<int:id>", methods=["DELETE"])
def deletar(id):
    try:
        supabase = connect_db()
        supabase.table("adolescentes").delete().eq("id", id).execute()
        return jsonify({"ok": True}), 200
    except Exception as e:
        print("ERRO DELETAR:", str(e))
        return jsonify({"erro": str(e)}), 500