import sys
import subprocess
from datetime import datetime
from pathlib import Path
import inspect
import os

# from .myconfigparser import MyConfigParser  # NOQA load this module here, otherwise following lines and sublines get error
try:
    import click
    from .lib_clickhelpers import AliasedGroup
except ImportError:
    click = None
from .tools import _file2env

from . import module_tools  # NOQA
from . import odoo_config  # NOQA

SCRIPT_DIRECTORY = Path(inspect.getfile(inspect.currentframe())).absolute().parent


os.environ["HOST_HOME"] = os.getenv("HOME", "")
os.environ["ODOO_HOME"] = str(SCRIPT_DIRECTORY)


from .cli import cli
from . import lib_clickhelpers  # NOQA
from . import lib_composer  # NOQA
from . import lib_backup  # NOQA
from . import lib_control  # NOQA
from . import lib_db  # NOQA
from . import lib_db_snapshots  # NOQA
from . import lib_lang  # NOQA
from . import lib_module  # NOQA
from . import lib_setup  # NOQA
from . import lib_src  # NOQA
from . import lib_docker_registry  # NOQA
from . import lib_turnintodev  # NOQA
from . import lib_talk  # NOQA
from . import lib_linting  # NOQA
from . import daddy_cleanup  # NOQA

# import container specific commands
from .tools import abort  # NOQA
from .tools import __dcrun  # NOQA
from .tools import __dc  # NOQA


@cli.command()
@click.option(
    "-x",
    "--execute",
    is_flag=True,
    help=("Execute the script to insert completion into users rc-file."),
)
def completion(execute):
    shell = os.environ["SHELL"].split("/")[-1]
    rc_file = Path(os.path.expanduser(f"~/.{shell}rc"))
    line = f'eval "$(_ODOO_COMPLETE={shell}_source odoo)"'
    if execute:
        content = rc_file.read_text().splitlines()
        if not list(
            filter(
                lambda x: line in x and not x.strip().startswith("#"),
                content,
            )
        ):
            content += [f"\n{line}\n"]
            click.secho(
                f"Inserted successfully\n{line}" "\n\nPlease restart you shell."
            )
            rc_file.write_text("\n".join(content))
        else:
            click.secho("Nothing done - already existed.")
    else:
        click.secho(
            "\n\n" f"Insert into {rc_file}\n\n" f"echo '{line}' >> {rc_file}" "\n\n"
        )
    sys.exit(0)


@cli.command()
@pass_config
def version(config):
    from .tools import _get_version

    version = _get_version()

    images_sha = subprocess.check_output(
        ["git", "log", "-n1", "--format=%H"], encoding="utf8", cwd=config.dirs["images"]
    ).strip()
    images_branch = subprocess.check_output(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        encoding="utf8",
        cwd=config.dirs["images"],
    ).strip()
    click.secho(
        (
            f"Wodoo Version:    {version}\n"
            f"Images SHA:       {images_sha}\n"
            f"Images Branch:    {images_branch}\n"
        ),
        fg="yellow",
    )
