from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/buy-stars", methods=["POST"])
def buy_stars():
    data = request.get_json()
    init_data = data.get("initData")

    # ❗ TODO: здесь нужно проверить подпись Telegram initData
    print(f"Покупка от Telegram: {init_data}")

    # ⚠️ Тут можно сохранить флаг "купил" в базу данных

    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(debug=True)
