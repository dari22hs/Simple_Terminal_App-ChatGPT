"""
Simple terminal app using ChatGPT API
"""
import config
import openai
import typer
from rich import print
from rich.table import Table


def main():
    """
    Main function of the app that asks the user for an input in order to reply by calling ChatGPT API
    """
    openai.api_key = config.api_key
    
    print("💬 [bold green]ChatGPT API en Python[/bold green]")

    table = Table("Comando", "Descripción")
    table.add_row("exit", "Salir de la aplicación.")
    table.add_row("new", "Crear una nueva conversación.")

    print(table)

    # Contexto del asistente
    context = {"role": "system",
               "content": "Eres un asistente muy útil."}
    messages = [context]

    while True:

        content = __prompt()

        if content == "new":
            print("📢 Nueva conversación creada.")
            messages = [context]
            content = __prompt()

        messages.append({"role": "user", "content": content})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages)

        response_content = response.choices[0].message.content

        messages.append({"role": "assistant", "content": response_content})

        print(f"[bold green]>[/bold green] [green]{response_content}[/green]")


def __prompt() -> str:
    prompt = typer.prompt("\n¿Sobre qué deseas hablar? ")

    if prompt == "exit":
        exit = typer.confirm("⚠️ ¿Desea salir?")
        if exit:
            print("👋 ¡Hasta luego!")
            raise typer.Abort()

        return __prompt()

    return prompt


if __name__ == "__main__":
    typer.run(main)
