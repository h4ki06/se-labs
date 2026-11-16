Lab 6 - Pet Boarding (PES2UG24CS180)

Place both test files and both screenshots in the repository's Lab 6 folder.

Run code coverage:
python -m pip install pytest coverage
python -m coverage erase
python -m coverage run -m pytest -q CodeCoverageTest_PES2UG24CS180_application.py
python -m coverage report -m

Run branch coverage:
python -m coverage erase
python -m coverage run --branch -m pytest -q BranchCoverageTest_PES2UG24CS180_application.py
python -m coverage report -m

Verified results:
- Code coverage: 100% (27 tests passed)
- Branch coverage: 100% (34 tests passed; 26/26 branches covered)

The tests import pet_boarding.py from the same folder. Do not rename that application file.
