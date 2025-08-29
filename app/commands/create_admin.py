import typer
from typing import Annotated
import asyncio
from app.core.use_cases import CreateAdminUserUseCase
from app.commands.cli_dependency import get_cli_user_repository

app = typer.Typer()

@app.command()
def create_admin(
    email: Annotated[str, typer.Option(..., prompt = True, help="Admin email")],
    password: Annotated[str, typer.Option(..., prompt=True, hide_input=True, confirmation_prompt=True, help="Admin password")],
    first_name: Annotated[str, typer.Option(..., prompt=True, help="First name")],
    last_name: Annotated[str, typer.Option(..., prompt=True, help="Last name")]
):
    async def run_command():
        user_repo = None
        try:
            user_repo = await get_cli_user_repository()
            use_case = CreateAdminUserUseCase(user_repo = user_repo)

            success = await use_case.execute(
                email=email,
                password=password,
                first_name= first_name,
                last_name = last_name
            )

            if success:
                typer.echo("Admin user created successfully")
                return True
            else:
                typer.echo("Failed to create admin user")
                return False
        except ValueError as e:
            typer.echo(f"Validation error: {e}")
            return False
        except Exception as e:
            typer.echo(f"Unexpected  error: {e}")
            return False
        finally:
            if user_repo:
                await user_repo.session.close()
    return asyncio.run(run_command())


if __name__ == '__main__':
    app()