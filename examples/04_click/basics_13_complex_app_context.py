import click
from rich import inspect


@click.group()
def dhcp_db():
    print("GROUP")


@dhcp_db.command()
@click.option("--db-schema", "-s", help="db schema filename")
@click.option("--db-filename", "-d", default="dhcp.db", help="db filename")
def create(db_schema, db_filename):
    """
    create DB
    """
    print(f"CREATE {db_schema=} {db_filename=}")


@dhcp_db.command()
@click.argument("filenames", nargs=-1, required=True)
@click.option("--db-filename", "-d", default="dhcp.db", help="db filename")
def add(filenames, db_filename):
    """
    add data to db from FILENAMES
    """
    print(f"ADD {filenames=} {db_filename=}")


@dhcp_db.command()
@click.option("--key", "-k", type=click.Choice(["mac", "ip", "vlan"]))
@click.option("--value", "-v", help="value of key")
@click.option("--db-filename", "-d", default="dhcp.db", help="db filename")
def get(key, value, db_filename):
    """
    get data from db
    """
    print(f"GET {key=} {value=} {db_filename=}")


if __name__ == "__main__":
    dhcp_db()
