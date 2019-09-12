import coverage

COV = coverage.coverage(
    branch=True,
    include='api/*',
    omit=[
        'api/tests/*',
        'api/config.py',
    ]
)
COV.start()
