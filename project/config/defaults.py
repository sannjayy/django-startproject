import os

ALLOW_PARALLEL_RUNS = True
if os.environ.get('ENABLE_TEST_PANEL', 'False').lower() == 'true':