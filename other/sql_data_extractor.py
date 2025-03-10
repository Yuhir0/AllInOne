import argparse
import clipboard
import sqlparse


def get_args():
    parser = argparse.ArgumentParser(description='SQL table and alias extractor.')
    parser.add_argument('-t', '--tables', action='store_true', help='Extract tables')
    parser.add_argument('-f', '--fields', action='store_true', help='Extract fields')
    args = parser.parse_args()
    return vars(args)


def extract_tables_and_aliases(sql):
    parsed = sqlparse.parse(sql)
    tables_and_aliases = []
    for statement in parsed:
        for token in statement.tokens:
            if isinstance(token, sqlparse.sql.Identifier):
                table_name = token.get_real_name()
                alias = token.get_alias()
                tables_and_aliases.append([table_name, alias])
    return tables_and_aliases


def main():
    args = get_args()
    sql = clipboard.paste()
    print(sql)
    match args:
        case {'tables': True}:
            print(extract_tables_and_aliases(sql))
        case _:
            print('No option selected')


if __name__ == '__main__':
    main()
