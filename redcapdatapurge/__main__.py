import dataset

import os
from dotenv import load_dotenv
load_dotenv()


def calculate_total_rows_count(db):
    total_rows_count = {}
    for table in db.tables:
        table_class = db.load_table(table)
        total_rows_count[table] = table_class.count()
    return total_rows_count


def cleanup_sql_for_delete_orphaned_projects_ids():
    sql_statements = []
    orphaned_project_ids = [19, 80, 81, 91, 103, 115, 116, 128, 129, 136, 144,
                            148, 152, 154, 156, 157, 158, 160, 172, 178, 183,
                            191, 194, 199, 200, 202, 207, 208, 209, 225, 229,
                            231, 250, 261, 262, 275]
    tables_with_orphans = [
        'redcap_actions', 'redcap_data_access_groups', 'redcap_data_dictionaries',
        'redcap_external_links', 'redcap_folders_projects',
        'redcap_library_map', 'redcap_locking_labels', 'redcap_metadata_prod_revisions',
        'redcap_mobile_app_devices', 'redcap_mobile_app_log', 'redcap_project_checklist',
        'redcap_record_counts', 'redcap_surveys_response_values', 'redcap_user_rights',
        'redcap_user_roles'
    ]

    orphaned_project_ids_string = ', '.join(str(x) for x in orphaned_project_ids)

    for table in tables_with_orphans:
        statement = f"DELETE FROM {table} WHERE project_id in ({orphaned_project_ids_string});"
        sql_statements.append(statement)

    return sql_statements


def cleanup_sql_for_delete_null_projects_ids():
    sql_statements = []
    tables_with_null_project_ids = [
        'redcap_external_module_settings'
    ]

    for table in tables_with_null_project_ids:
        statement = f"DELETE FROM {table} WHERE project_id IS NULL;"
        sql_statements.append(statement)

    return sql_statements


def cleanup_sql_for_delete_null_ui_ids():
    sql_statements = []
    tables_with_null_ui_ids = [
        {'table': 'redcap_messages', 'field': 'author_user_id'},
        {'table': 'redcap_messages_recipients', 'field': 'recipient_user_id'},
        {'table': 'redcap_surveys_themes', 'field': 'ui_id'},
    ]

    for t in tables_with_null_ui_ids:
        table = t['table']
        field = t['field']
        statement = f"DELETE FROM {table} WHERE {field} IS NULL;"
        sql_statements.append(statement)

    return sql_statements


def cleanup_sql_for_other_orphans():
    sql_statements = []

    tables_with_orphans = [
        {
            'table': 'redcap_docs_to_edocs',
            'field': 'docs_id',
            'ids': [166, 1321, 1322, 1558, 2255, 2256, 2257, 2349, 2350, 2351, 2352, 2353, 2354, 2374, 2997, 3064]
        },
        {
            'table': 'redcap_events_forms',
            'field': 'event_id',
            'ids': [388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407,
                    408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 534, 535, 536, 537,
                    538, 539, 540, 541, 542, 543, 544, 545, 546, 547, 548, 549, 550, 551, 552, 620, 622, 623, 624, 625,
                    626, 627, 628, 629, 630, 631, 632, 633, 634, 838, 839, 846, 847, 848, 849, 850, 851, 852, 853, 876,
                    880, 886, 887, 888, 889, 890, 891, 892, 893, 894, 895, 896, 898, 899, 900, 901, 902, 903, 904, 905,
                    906, 907, 908, 910, 911, 912, 935, 936, 937, 938, 939, 940, 941, 942, 943, 944, 945, 990, 1029,
                    1030, 1031, 1032, 1033, 1034, 1035, 1036, 1037, 1041, 1088, 1089, 1091, 1097, 1098, 1133, 1142,
                    1144, 1208, 1252, 1253, 1254, 1255, 1256, 1257, 1258, 1259, 1260, 1261, 1282, 1283, 1284, 1285,
                    1286]
        },
        {
            'table': 'redcap_events_repeat',
            'field': 'event_id',
            'ids': [388, 393, 394, 399, 400, 401, 402, 403, 404, 405, 406, 411, 412, 417, 418, 419, 420, 421, 422, 423,
                    534, 540, 541, 546, 547, 548, 549, 550, 551, 552, 620, 622, 623, 624, 625, 626, 627, 628, 629, 630,
                    631, 632, 633, 634]
        },
        {
            'table': 'redcap_randomization_allocation',
            'field': 'rid',
            'ids': [18]
        },
        {
            'table': 'redcap_reports_access_roles',
            'field': 'report_id',
            'ids': [278, 279, 304]
        },
        {
            'table': 'redcap_reports_access_users',
            'field': 'report_id',
            'ids': [305, 306, 307, 314, 315, 316, 319, 320, 321, 322, 323, 324, 325, 330, 334, 336]
        },
        {
            'table': 'redcap_reports_fields',
            'field': 'report_id',
            'ids': [87, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111,
                    112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 270, 271, 272, 273, 274,
                    275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294,
                    295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314,
                    315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334,
                    335, 336, 435, 439, 440, 445, 446, 447, 461, 463, 491, 495, 496, 501, 502, 503, 517, 519, 568, 569,
                    572, 573, 574, 779, 882]
        },
        {
            'table': 'redcap_reports_filter_events',
            'field': 'report_id',
            'ids': [91, 92, 93, 94, 95, 96, 97, 98, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112,
                    113, 114, 115, 116, 117, 118, 121, 122, 124, 126, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279,
                    281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300,
                    301, 302, 303, 305, 306, 307, 309, 310, 311, 312, 314, 315, 316, 318, 319, 320, 321, 324, 326, 327,
                    328, 329, 331, 332, 333, 334, 336]
        },
        {
            'table': 'redcap_surveys_emails_recipients',
            'field': 'email_recip_id',
            'ids': [736, 737, 749, 750, 751, 3185, 3186, 3187, 3188, 3189, 3190, 3191, 3192, 3193, 3194, 3195, 3196,
                    3197, 3198, 3199, 3200, 3202, 3203, 3204, 3205, 3206, 3207, 3208, 3209, 3210, 3211, 3212, 3213,
                    3214, 3215, 3217, 3218, 3219, 3220, 3221, 3222, 3223, 3224, 3225, 3226, 3881, 3882, 3883, 4153,
                    4154, 5102, 5699, 5700, 5701, 8368, 8369, 8370, 8371, 8415, 9064, 9065]
        },
        {
            'table': 'redcap_surveys_queue',
            'field': 'survey_id',
            'ids': [348, 356, 390, 398, 484, 492, 1123, 1150, 1200, 1388, 1389, 1390]
        },
        {
            'table': 'redcap_surveys_response_users',
            'field': 'response_id',
            'ids': [71003, 71008, 71009, 71010, 71011, 71012, 71013, 71017, 71023, 71025, 71030, 71031, 71033, 71034,
                    71035, 71036, 71038, 71040, 71041, 71044, 71045, 71046, 71047, 71048, 71053, 71054, 71057, 71059,
                    71061, 71062, 71063, 71064, 76841, 79235, 79236, 79238, 79243, 84149, 85019, 85032, 86987, 87530,
                    91892, 93163, 93176, 93184, 93187, 93191]
        },
        {
            'table': 'redcap_surveys_scheduler',
            'field': 'event_id',
            'ids': [58, 67]
        },
        {
            'table': 'redcap_surveys_scheduler_queue',
            'field': 'email_recip_id',
            'ids': [736, 737, 749, 750, 751, 3185, 3186, 3187, 3188, 3189, 3190, 3191, 3192, 3193, 3194, 3195, 3196,
                    3197, 3198, 3199, 3200, 3202, 3203, 3204, 3205, 3206, 3207, 3208, 3209, 3210, 3211, 3212, 3213,
                    3214, 3215, 3217, 3218, 3219, 3220, 3221, 3222, 3223, 3224, 3225, 3226, 3881, 3882, 4153, 4154,
                    5102, 5699, 5700, 5701, 8369, 8370, 8415, 9064]
        },
    ]

    for t in tables_with_orphans:
        table = t['table']
        field = t['field']
        ids = t['ids']
        ids_string = ', '.join(str(x) for x in ids)
        statement = f"DELETE FROM {table} WHERE {field} in ({ids_string});"
        sql_statements.append(statement)

    return sql_statements


def verify_empty_tables(table_row_count):
    """
    Verifies that the expected tables have no entries, as they are not
    processed by the script.
    """
    expected_empty_tables = {
        'redcap_external_modules_log',
        'redcap_external_modules_log_parameters',
        'redcap_instrument_zip',
        'redcap_instrument_zip_authors',
        'redcap_ip_banned',
        'redcap_projects_external',
        'redcap_pub_articles',
        'redcap_pub_authors',
        'redcap_pub_matches',
        'redcap_pub_mesh_terms',
        'redcap_user_whitelist'
    }

    for t in expected_empty_tables:
        try:
            count_for_table = table_row_count[t]
            if count_for_table is None:
                print(f"ERROR: Expected empty table '{t}' not found in row count.")
                exit(1)
            if count_for_table != 0:
                print(f"Error: Expected empty table '{t}' had {count_for_table} rows.")
                exit(1)
        except KeyError:
            print(f"ERROR: Expected empty table '{t}' not found in row count.")
            exit(1)


def purge_sql_for_redcap_projects(project_ids_to_keep):
    sql_statements = []

    tables = [
        'redcap_projects'
    ]

    project_ids_to_keep_string = ', '.join(str(x) for x in project_ids_to_keep)

    for table in tables:
        statement = f"DELETE FROM {table} WHERE project_id NOT in ({project_ids_to_keep_string});"
        sql_statements.append(statement)

    return sql_statements


def purge_sql_for_redcap_user_information(user_names_to_keep):
    sql_statements = []

    tables = [
        'redcap_user_information'
    ]

    user_names_to_keep_string = ', '.join(f"'{str(x)}'" for x in user_names_to_keep)

    for table in tables:
        statement = f"DELETE FROM {table} WHERE username NOT in ({user_names_to_keep_string});"
        sql_statements.append(statement)

    return sql_statements


def purge_sql_unattached_tables_with_project_id(project_ids_to_keep):
    sql_statements = []

    tables = [
        'redcap_data',
        'redcap_edocs_metadata',
        'redcap_log_event',
    ]

    project_ids_to_keep_string = ', '.join(str(x) for x in project_ids_to_keep)

    for table in tables:
        statement = f"DELETE FROM {table} WHERE project_id NOT in ({project_ids_to_keep_string});"
        sql_statements.append(statement)

    return sql_statements


def purge_sql_unattached_tables_with_user_name(user_names_to_keep):
    sql_statements = []

    tables = [
        'redcap_auth',
        'redcap_auth_history',
        'redcap_sendit_docs',
    ]

    user_names_to_keep_string = ', '.join(f"'{str(x)}'" for x in user_names_to_keep)

    for table in tables:
        statement = f"DELETE FROM {table} WHERE username NOT in ({user_names_to_keep_string});"
        sql_statements.append(statement)

    return sql_statements


def main():
    required_env_vars = ["DB_URL", "SUMMARY_OUTPUT_FILE",
                         "PURGE_QUERIES_OUTPUT_FILE", "RELATED_ITEM_IDS_OUTPUT_FILE"]
    for var in required_env_vars:
        if not os.getenv(var):
            print(f"Required environment variable '{var}' is missing.")
            exit(1)

    cleanup_sql_statements = []
    cleanup_sql_statements.extend(cleanup_sql_for_delete_orphaned_projects_ids())
    cleanup_sql_statements.extend(cleanup_sql_for_delete_null_projects_ids())
    cleanup_sql_statements.extend(cleanup_sql_for_delete_null_ui_ids())
    cleanup_sql_statements.extend(cleanup_sql_for_other_orphans())

    cleanup_file = os.getenv("CLEANUP_OUTPUT_FILE")
    with open(cleanup_file, 'w') as fp:
        fp.write('\n'.join(cleanup_sql_statements))

    # Get values from .env config file
    db_url = os.getenv("DB_URL")
    db = dataset.connect(db_url)

    total_rows_count = calculate_total_rows_count(db)
    print(f"total_rows_count: {total_rows_count}")
    verify_empty_tables(total_rows_count)

    usernames_to_keep = [
        'dyarnell', 'dmilton', 'sbobbin', 'jbueno', 'balbert', 'rwashing',
        'sy344', 'dmilton2', 'adenaiye', 'vdemaio', 'imoleayof19', 'amarafox',
        'tgold', 'stefanos', 'Ali98', 'lynch17', 'magidya', 'mmistret',
        'tomiokanlawon', 'abhipat', 'micah38', 'melaynap', 'shirarubin37',
        'jsolow', 'cstipa', 'msuh1145', 'sswanzy04', 'Lwakefie', 'jmarron',
        'fhong', 'gmagno', 'rezeugoh', 'dmilton_api', 'jgerman', 'calilung',
        'dsteelma', 'durden']

    project_ids_to_keep = [
        35, 36, 38, 39, 40, 41, 42, 47, 48, 49, 50, 52, 54, 55, 58, 60, 61, 63,
        64, 65, 66, 67, 68, 73, 82, 89, 90, 92, 94, 99, 100, 101, 110, 117, 118,
        119, 120, 123, 124, 179, 180, 311
    ]

    purge_sql_statements = []
    purge_sql_statements.append('-- purge_sql_for_redcap_projects')
    purge_sql_statements.extend(purge_sql_for_redcap_projects(project_ids_to_keep))
    purge_sql_statements.append('-- purge_sql_for_redcap_user_information')
    purge_sql_statements.extend(purge_sql_for_redcap_user_information(usernames_to_keep))
    purge_sql_statements.append('-- purge_sql_unattached_tables_with_project_id')
    purge_sql_statements.extend(purge_sql_unattached_tables_with_project_id(project_ids_to_keep))
    purge_sql_statements.append('-- purge_sql_unattached_tables_with_user_name')
    purge_sql_statements.extend(purge_sql_unattached_tables_with_user_name(usernames_to_keep))

    purge_queries_file = os.getenv("PURGE_QUERIES_OUTPUT_FILE")
    with open(purge_queries_file, 'w') as fp:
        fp.write('\n'.join(purge_sql_statements))


if __name__ == '__main__':
    main()

