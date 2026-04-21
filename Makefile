PYTHONPATH=src

install:
	pip install -r requirements.txt
	pip install -e .

benchmark:
	$(PYTHONPATH) python scripts/run_full_study.py

assets:
	$(PYTHONPATH) python scripts/generate_report_assets.py

dashboard:
	$(PYTHONPATH) python scripts/build_dashboard.py

test:
	pytest -q
