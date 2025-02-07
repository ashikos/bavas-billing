import os
import subprocess
from datetime import datetime
from django.conf import settings


def get_psql_dump_file():
    """
    Generates a PostgreSQL database dump file based on Django settings.

    Returns:
        str: The path to the generated dump file.
    """
    # Define the output folder where the dump will be saved
    output_folder = os.path.join(settings.BASE_DIR, 'db_dumps')
    os.makedirs(output_folder, exist_ok=True)  # Ensure the folder exists

    # Database configuration from Django settings
    db_config = settings.DATABASES['default']

    # Extract PostgreSQL connection details
    host = db_config.get('HOST', 'localhost')
    port = db_config.get('PORT', '5432')
    user = db_config.get('USER')
    password = db_config.get('PASSWORD')
    database = db_config.get('NAME')

    # Ensure all required keys are present
    if not all([host, port, user, password, database]):
        raise ValueError("Database configuration is missing required keys.")

    # Generate a timestamped dump file name
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    dump_file = os.path.join(output_folder, f"{database}_dump_{timestamp}.sql")

    # Set the password in the environment for `pg_dump` (to avoid prompting for it)
    env = os.environ.copy()
    env['PGPASSWORD'] = password

    # Construct the `pg_dump` command
    command = (
        f"pg_dump -h {host} -p {port} -U {user} -d {database} -F p > {dump_file}"
    )

    # Execute the command
    result = subprocess.run(command, shell=True, env=env, text=True, capture_output=True)

    if result.returncode != 0:
        raise RuntimeError(f"Database dump failed: {result.stderr}")

    print(f"Database dump created successfully: {dump_file}")
    return dump_file
