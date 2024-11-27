import os
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

telbot = "TOKEN_BOT_AQUI_MEU_FILHO"
dirzao = r"CAMINHO_DA_SUA_PASTA_VEI_PLMDS"

usuariodedroga = {}

async def pesquisar(update: Update, context: ContextTypes.DEFAULT_TYPE, termo: str) -> None:
    user_id = update.message.from_user.id
    usuariodedroga[user_id] = {'termo': termo}
    resultados = []

    for root, dirs, files in os.walk(dirzao):
        for file in files:
            if file in ["passwords.txt", "All Passwords.txt", "Passwords.txt"]:
                caminhone = os.path.join(root, file)

                try:
                    with open(caminhone, "r", encoding="utf-8") as f:
                        conteudo = f.read().lower()
                except UnicodeDecodeError:
                    try:
                        with open(caminhone, "r", encoding="latin-1") as f:
                            conteudo = f.read().lower()
                    except UnicodeDecodeError:
                        continue

                linhas = conteudo.splitlines()
                info = ""
                user_info = ""
                pass_info = ""

                for i, linha in enumerate(linhas):
                    if "url:" in linha:
                        info = linha + "\n"
                    if (("login:" in linha or "user:" in linha) and termo in linha) or (("email:" in linha) and termo in linha):
                        user_info = linha.replace("login:", "USER:").replace("user:", "USER:").strip() + "\n"
                    if "password:" in linha or "pass:" in linha:
                        pass_info = linha.replace("password:", "PASS:").replace("pass:", "PASS:").strip()

                    if info and user_info and pass_info:
                        resultados.append(info + user_info + pass_info)
                        info = ""
                        user_info = ""
                        pass_info = ""

    if resultados:
        caminho_arquivo = os.path.join(dirzao, f"resultado_pesquisa_{user_id}.txt")
        with open(caminho_arquivo, "w", encoding="utf-8") as f:
            f.write("\n\n".join(resultados))

        with open(caminho_arquivo, "rb") as arquivo:
            await update.message.reply_document(document=InputFile(arquivo), filename=f"resultado_{termo}.txt")
    else:
        resposta = "❌ Nenhum resultado encontrado senhor(a): " + termo
        await update.message.reply_text(resposta)

async def pesquisar_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    termo = context.args[0].lower() if len(context.args) > 0 else None
    if termo:
        await pesquisar(update, context, termo)
    else:
        await update.message.reply_text("✅ Por favor, forneça um email para pesquisa\nEx: /email <email>")

async def pesquisar_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    termo = context.args[0].lower() if len(context.args) > 0 else None
    if termo:
        await pesquisar(update, context, termo)
    else:
        await update.message.reply_text("✅ Por favor, forneça um usuário para pesquisa\nEx: /user <usuario>")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("🖥️ *BOT SEARCH!*\n\nPara procurar url use /pesquisar <palavrachave>\nPara procurar um email use /email <email>\nPara procurar um usuário use /user <usuario>", parse_mode="Markdown")

def main() -> None:
    application = ApplicationBuilder().token(telbot).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("pesquisar", pesquisar_email))
    application.add_handler(CommandHandler("email", pesquisar_email))
    application.add_handler(CommandHandler("user", pesquisar_user))

    application.run_polling()

if __name__ == '__main__':
    main()
