import typer
from app.models.user import User, UserBase
from app.database import create_db_and_tables, get_cli_session, drop_all
from sqlmodel import select

cli = typer.Typer()

@cli.command()
def initialize():
    with get_cli_session() as db:
        drop_all()
        create_db_and_tables()
    
        user1 = User(
            username="bob",
            email="bob@email.com",
            password="bobpass",
            role="student"
        )

        db.add(user1)
        db.commit()

        typer.echo("Database Initialize!")



if __name__ == "__main__":
    cli()