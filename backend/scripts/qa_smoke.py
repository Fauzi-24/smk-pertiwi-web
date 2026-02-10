import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from backend.app.services.gemini_service import SMKPertiwiChatbot


def build_tests(bot):
    data = bot.school_data
    tests = []

    headmaster = data.get("headmaster")
    if headmaster:
        tests.append(("siapa kepala sekolah smk pertiwi kuningan", [headmaster]))

    address = data.get("address")
    if address:
        tests.append(("alamat smk pertiwi kuningan", [address]))

    advantages = data.get("advantages", [])
    if advantages:
        tests.append(("apa keunggulan sekolah", [advantages[0]]))

    schedule = data.get("schedule", [])
    if schedule:
        tests.append(("jadwal pelajaran", [schedule[0]]))

    majors = data.get("majors", [])
    if majors:
        tests.append(("jurusan apa saja", [majors[0].get("kode", "")]))

    teachers = data.get("teachers", [])
    if teachers and majors:
        kode = majors[0].get("kode")
        names = bot._get_teachers_by_major(teachers, kode)
        if names:
            tests.append((f"siapa guru {kode}", [names[0]]))

    return tests


if __name__ == "__main__":
    bot = SMKPertiwiChatbot()
    tests = build_tests(bot)
    print(f"Running {len(tests)} tests...\n")

    passed = 0
    for idx, (query, expected_list) in enumerate(tests, start=1):
        answer = bot._try_answer_from_data(query) or ""
        ok = any(expected.lower() in answer.lower() for expected in expected_list if expected)
        status = "PASS" if ok else "FAIL"
        print(f"{idx}. {status} | {query}")
        if not ok:
            print(f"   Expected one of: {expected_list}")
            print(f"   Answer: {answer}")
        if ok:
            passed += 1

    print(f"\nPassed {passed}/{len(tests)} tests")
