setup:
	pip install -r requirements.txt || true

test:
	docker build -t chimera-test .
	docker run --rm chimera-test

spec-check:
	@echo "Spec alignment check not yet implemented"
