# Find a feasible solution satisfying EF1-CC+ and capacity constraints, only for "small public dataset".
from gurobipy import *
import time
import csv

from gurobipy import *
import json
import time

def generate_conflicts_from_timings(course_timings):
    """Generate course conflicts based on overlapping time slots"""
    conflicts = {}
    for course1, timing1 in course_timings.items():
        conflicts[course1] = []
        for course2, timing2 in course_timings.items():
            if course1 != course2:
                start1, end1 = timing1["start_time"], timing1["end_time"]
                start2, end2 = timing2["start_time"], timing2["end_time"]
                if not (end1 <= start2 or end2 <= start1):
                    conflicts[course1].append(course2)
    return conflicts

def solve_ef_allocation():
    #load data: course timings–[asted from genertaed json, course data from the github repo
    with open('course_timings.json', 'r') as f:
        timing_data = {
            "course_timings": {
                "dHyst ntvnym byvm b 9:00": {
                "start_time": 3,
                "end_time": 4,
                "duration": 1,
                "capacity": 126
                },
                "dHyst ntvnym byvm g 14:00": {
                "start_time": 8,
                "end_time": 9,
                "duration": 1,
                "capacity": 40
                },
                "ptrvn b`yvt bAmTS`vt HypvSH": {
                "start_time": 7,
                "end_time": 8,
                "duration": 1,
                "capacity": 82
                },
                "Algvrytmym KHlKHlyym": {
                "start_time": 3,
                "end_time": 6,
                "duration": 3,
                "capacity": 44
                },
                "lmydh yySHvmyt brAyyh mmvHSHbt byvm d 15:00": {
                "start_time": 17,
                "end_time": 18,
                "duration": 1,
                "capacity": 50
                },
                "lmydh yySHvmyt brAyyh mmvHSHbt byvm h 15:00": {
                "start_time": 13,
                "end_time": 14,
                "duration": 1,
                "capacity": 50
                },
                "rvbvTym AvTvnvmyym": {
                "start_time": 0,
                "end_time": 1,
                "duration": 1,
                "capacity": 69
                },
                "hskh sTTysTyt": {
                "start_time": 6,
                "end_time": 7,
                "duration": 1,
                "capacity": 80
                },
                "nvSHAym mtkdmym brAyyh mmvHSHbt `m yySHvmym bhdmyh rpvAyt": {
                "start_time": 16,
                "end_time": 19,
                "duration": 3,
                "capacity": 40
                },
                "SHyTvt lgylvy htkpvt syybr": {
                "start_time": 0,
                "end_time": 3,
                "duration": 3,
                "capacity": 55
                },
                "nytvH myd` bmymdym gbvhym": {
                "start_time": 6,
                "end_time": 9,
                "duration": 3,
                "capacity": 77
                },
                "gyAvmTryh bdydh": {
                "start_time": 17,
                "end_time": 19,
                "duration": 2,
                "capacity": 67
                },
                "lmydt mKHvnh": {
                "start_time": 7,
                "end_time": 9,
                "duration": 2,
                "capacity": 81
                },
                "sybvKHyvt tkSHvrt": {
                "start_time": 8,
                "end_time": 9,
                "duration": 1,
                "capacity": 50
                },
                "lmydh `mvkh v`ybvd SHpvt Tb`yvt": {
                "start_time": 5,
                "end_time": 8,
                "duration": 3,
                "capacity": 86
                },
                "tAvryh SHl krypTvgrpyh": {
                "start_time": 13,
                "end_time": 15,
                "duration": 2,
                "capacity": 50
                },
                "spykvt bvlyAnyt": {
                "start_time": 8,
                "end_time": 9,
                "duration": 1,
                "capacity": 40
                },
                "Algvrytmym bbynh mlAKHvtyt": {
                "start_time": 6,
                "end_time": 8,
                "duration": 2,
                "capacity": 84
                },
                "prTyvt HySHvb": {
                "start_time": 3,
                "end_time": 4,
                "duration": 1,
                "capacity": 65
                },
                "mbvA lkrypTvgrpyh": {
                "start_time": 12,
                "end_time": 13,
                "duration": 1,
                "capacity": 50
                },
                "pytvH mSHHky mHSHb": {
                "start_time": 11,
                "end_time": 13,
                "duration": 2,
                "capacity": 40
                },
                "tKHnvt Algvrytmym mHkryym": {
                "start_time": 8,
                "end_time": 9,
                "duration": 1,
                "capacity": 41
                },
                "nvSHAym mtkdmym btvrt hgrpym": {
                "start_time": 14,
                "end_time": 17,
                "duration": 3,
                "capacity": 40
                }
            },
            "parameters": {
                "total_school_time": 20,
                "num_courses": 23,
                "num_students": 26,
                "random_seed": 42
            }
        }

    # Generate conflicts from timings
    item_conflicts = generate_conflicts_from_timings(timing_data["course_timings"])
    # Load the data
    data = {"valuations": {"s64": {"lmydt mKHvnh": 501, "hskh sTTysTyt": 211, "SHyTvt lgylvy htkpvt syybr": 112, "rvbvTym AvTvnvmyym": 64, "prTyvt HySHvb": 47, "nvSHAym mtkdmym brAyyh mmvHSHbt `m yySHvmym bhdmyh rpvAyt": 40, "tAvryh SHl krypTvgrpyh": 6, "dHyst ntvnym byvm b 9:00": 0, "ptrvn b`yvt bAmTS`vt HypvSH": 0, "Algvrytmym KHlKHlyym": 0, "lmydh yySHvmyt brAyyh mmvHSHbt byvm d 15:00": 0, "nytvH myd` bmymdym gbvhym": 0, "gyAvmTryh bdydh": 0, "sybvKHyvt tkSHvrt": 0, "lmydh `mvkh v`ybvd SHpvt Tb`yvt": 0, "spykvt bvlyAnyt": 0, "Algvrytmym bbynh mlAKHvtyt": 0}, "s67": {"dHyst ntvnym byvm b 9:00": 170, "ptrvn b`yvt bAmTS`vt HypvSH": 0, "Algvrytmym KHlKHlyym": 166, "lmydh yySHvmyt brAyyh mmvHSHbt byvm d 15:00": 0, "rvbvTym AvTvnvmyym": 0, "hskh sTTysTyt": 166, "nvSHAym mtkdmym brAyyh mmvHSHbt `m yySHvmym bhdmyh rpvAyt": 0, "SHyTvt lgylvy htkpvt syybr": 0, "nytvH myd` bmymdym gbvhym": 0, "gyAvmTryh bdydh": 0, "lmydt mKHvnh": 0, "sybvKHyvt tkSHvrt": 0, "lmydh `mvkh v`ybvd SHpvt Tb`yvt": 166, "prTyvt HySHvb": 0, "tAvryh SHl krypTvgrpyh": 0, "spykvt bvlyAnyt": 166, "Algvrytmym bbynh mlAKHvtyt": 0}, "s68": {"nvSHAym mtkdmym brAyyh mmvHSHbt `m yySHvmym bhdmyh rpvAyt": 204, "rvbvTym AvTvnvmyym": 163, "lmydh yySHvmyt brAyyh mmvHSHbt byvm d 15:00": 145, "SHyTvt lgylvy htkpvt syybr": 127, "nytvH myd` bmymdym gbvhym": 109, "hskh sTTysTyt": 90, "lmydt mKHvnh": 72, "Algvrytmym KHlKHlyym": 54, "Algvrytmym bbynh mlAKHvtyt": 36, "dHyst ntvnym byvm b 9:00": 0, "ptrvn b`yvt bAmTS`vt HypvSH": 0, "gyAvmTryh bdydh": 0, "sybvKHyvt tkSHvrt": 0, "lmydh `mvkh v`ybvd SHpvt Tb`yvt": 0, "prTyvt HySHvb": 0, "tAvryh SHl krypTvgrpyh": 0, "spykvt bvlyAnyt": 0}, "s69": {"dHyst ntvnym byvm b 9:00": 250, "lmydh `mvkh v`ybvd SHpvt Tb`yvt": 250, "nytvH myd` bmymdym gbvhym": 250, "ptrvn b`yvt bAmTS`vt HypvSH": 0, "Algvrytmym KHlKHlyym": 0, "lmydh yySHvmyt brAyyh mmvHSHbt byvm d 15:00": 0, "rvbvTym AvTvnvmyym": 0, "hskh sTTysTyt": 0, "nvSHAym mtkdmym brAyyh mmvHSHbt `m yySHvmym bhdmyh rpvAyt": 0, "SHyTvt lgylvy htkpvt syybr": 0, "gyAvmTryh bdydh": 0, "lmydt mKHvnh": 0, "sybvKHyvt tkSHvrt": 0, "prTyvt HySHvb": 0, "tAvryh SHl krypTvgrpyh": 0, "spykvt bvlyAnyt": 0, "Algvrytmym bbynh mlAKHvtyt": 0}, "s71": {"dHyst ntvnym byvm b 9:00": 288, "dHyst ntvnym byvm g 14:00": 0, "ptrvn b`yvt bAmTS`vt HypvSH": 0, "Algvrytmym KHlKHlyym": 0, "lmydh yySHvmyt brAyyh mmvHSHbt byvm d 15:00": 0, "lmydh yySHvmyt brAyyh mmvHSHbt byvm h 15:00": 0, "rvbvTym AvTvnvmyym": 0, "hskh sTTysTyt": 249, "nvSHAym mtkdmym brAyyh mmvHSHbt `m yySHvmym bhdmyh rpvAyt": 201, "SHyTvt lgylvy htkpvt syybr": 0, "nytvH myd` bmymdym gbvhym": 0, "gyAvmTryh bdydh": 0, "lmydt mKHvnh": 262, "sybvKHyvt tkSHvrt": 0, "lmydh `mvkh v`ybvd SHpvt Tb`yvt": 0, "tAvryh SHl krypTvgrpyh": 0, "spykvt bvlyAnyt": 0, "Algvrytmym bbynh mlAKHvtyt": 0, "prTyvt HySHvb": 0, "mbvA lkrypTvgrpyh": 0, "pytvH mSHHky mHSHb": 0, "tKHnvt Algvrytmym mHkryym": 0, "nvSHAym mtkdmym btvrt hgrpym": 0}, "s76": {"dHyst ntvnym byvm b 9:00": 0, "dHyst ntvnym byvm g 14:00": 103, "ptrvn b`yvt bAmTS`vt HypvSH": 0, "Algvrytmym KHlKHlyym": 0, "lmydh yySHvmyt brAyyh mmvHSHbt byvm d 15:00": 0, "lmydh yySHvmyt brAyyh mmvHSHbt byvm h 15:00": 0, "rvbvTym AvTvnvmyym": 144, "hskh sTTysTyt": 0, "nvSHAym mtkdmym brAyyh mmvHSHbt `m yySHvmym bhdmyh rpvAyt": 0, "SHyTvt lgylvy htkpvt syybr": 237, "nytvH myd` bmymdym gbvhym": 0, "gyAvmTryh bdydh": 0, "lmydt mKHvnh": 0, "sybvKHyvt tkSHvrt": 0, "lmydh `mvkh v`ybvd SHpvt Tb`yvt": 0, "tAvryh SHl krypTvgrpyh": 0, "spykvt bvlyAnyt": 0, "Algvrytmym bbynh mlAKHvtyt": 0, "prTyvt HySHvb": 0, "mbvA lkrypTvgrpyh": 0, "pytvH mSHHky mHSHb": 440, "tKHnvt Algvrytmym mHkryym": 76, "nvSHAym mtkdmym btvrt hgrpym": 0}, "s78": {"lmydh `mvkh v`ybvd SHpvt Tb`yvt": 600, "lmydt mKHvnh": 400, "lmydh yySHvmyt brAyyh mmvHSHbt byvm d 15:00": 0, "dHyst ntvnym byvm b 9:00": 0, "dHyst ntvnym byvm g 14:00": 0, "ptrvn b`yvt bAmTS`vt HypvSH": 0, "Algvrytmym KHlKHlyym": 0, "lmydh yySHvmyt brAyyh mmvHSHbt byvm h 15:00": 0, "rvbvTym AvTvnvmyym": 0, "hskh sTTysTyt": 0, "nvSHAym mtkdmym brAyyh mmvHSHbt `m yySHvmym bhdmyh rpvAyt": 0, "SHyTvt lgylvy htkpvt syybr": 0, "nytvH myd` bmymdym gbvhym": 0, "gyAvmTryh bdydh": 0, "sybvKHyvt tkSHvrt": 0, "tAvryh SHl krypTvgrpyh": 0, "spykvt bvlyAnyt": 0, "Algvrytmym bbynh mlAKHvtyt": 0, "prTyvt HySHvb": 0, "mbvA lkrypTvgrpyh": 0, "pytvH mSHHky mHSHb": 0, "tKHnvt Algvrytmym mHkryym": 0, "nvSHAym mtkdmym btvrt hgrpym": 0}, "s80": {"nvSHAym mtkdmym brAyyh mmvHSHbt `m yySHvmym bhdmyh rpvAyt": 395, "dHyst ntvnym byvm b 9:00": 350, "nytvH myd` bmymdym gbvhym": 131, "Algvrytmym KHlKHlyym": 124, "hskh sTTysTyt": 0, "dHyst ntvnym byvm g 14:00": 0, "lmydh yySHvmyt brAyyh mmvHSHbt byvm d 15:00": 0, "ptrvn b`yvt bAmTS`vt HypvSH": 0, "lmydh yySHvmyt brAyyh mmvHSHbt byvm h 15:00": 0, "rvbvTym AvTvnvmyym": 0, "SHyTvt lgylvy htkpvt syybr": 0, "gyAvmTryh bdydh": 0, "lmydt mKHvnh": 0, "sybvKHyvt tkSHvrt": 0, "lmydh `mvkh v`ybvd SHpvt Tb`yvt": 0, "tAvryh SHl krypTvgrpyh": 0, "spykvt bvlyAnyt": 0, "Algvrytmym bbynh mlAKHvtyt": 0, "prTyvt HySHvb": 0, "mbvA lkrypTvgrpyh": 0, "pytvH mSHHky mHSHb": 0, "tKHnvt Algvrytmym mHkryym": 0, "nvSHAym mtkdmym btvrt hgrpym": 0}, "s81": {"dHyst ntvnym byvm b 9:00": 168, "dHyst ntvnym byvm g 14:00": 168, "ptrvn b`yvt bAmTS`vt HypvSH": 0, "Algvrytmym KHlKHlyym": 0, "lmydh yySHvmyt brAyyh mmvHSHbt byvm d 15:00": 0, "lmydh yySHvmyt brAyyh mmvHSHbt byvm h 15:00": 0, "rvbvTym AvTvnvmyym": 0, "hskh sTTysTyt": 0, "nvSHAym mtkdmym brAyyh mmvHSHbt `m yySHvmym bhdmyh rpvAyt": 0, "SHyTvt lgylvy htkpvt syybr": 166, "nytvH myd` bmymdym gbvhym": 0, "gyAvmTryh bdydh": 166, "lmydt mKHvnh": 166, "sybvKHyvt tkSHvrt": 0, "lmydh `mvkh v`ybvd SHpvt Tb`yvt": 0, "tAvryh SHl krypTvgrpyh": 0, "spykvt bvlyAnyt": 0, "Algvrytmym bbynh mlAKHvtyt": 0, "prTyvt HySHvb": 0, "mbvA lkrypTvgrpyh": 0, "pytvH mSHHky mHSHb": 166, "tKHnvt Algvrytmym mHkryym": 0, "nvSHAym mtkdmym btvrt hgrpym": 0}, "s83": {"dHyst ntvnym byvm b 9:00": 280, "dHyst ntvnym byvm g 14:00": 0, "ptrvn b`yvt bAmTS`vt HypvSH": 40, "Algvrytmym KHlKHlyym": 0, "lmydh yySHvmyt brAyyh mmvHSHbt byvm d 15:00": 0, "lmydh yySHvmyt brAyyh mmvHSHbt byvm h 15:00": 5, "rvbvTym AvTvnvmyym": 0, "hskh sTTysTyt": 0, "nvSHAym mtkdmym brAyyh mmvHSHbt `m yySHvmym bhdmyh rpvAyt": 103, "SHyTvt lgylvy htkpvt syybr": 0, "nytvH myd` bmymdym gbvhym": 0, "gyAvmTryh bdydh": 0, "lmydt mKHvnh": 199, "sybvKHyvt tkSHvrt": 0, "lmydh `mvkh v`ybvd SHpvt Tb`yvt": 190, "tAvryh SHl krypTvgrpyh": 0, "spykvt bvlyAnyt": 0, "Algvrytmym bbynh mlAKHvtyt": 183, "prTyvt HySHvb": 0, "mbvA lkrypTvgrpyh": 0, "pytvH mSHHky mHSHb": 0, "tKHnvt Algvrytmym mHkryym": 0, "nvSHAym mtkdmym btvrt hgrpym": 0}, "s84": {"lmydt mKHvnh": 200, "lmydh `mvkh v`ybvd SHpvt Tb`yvt": 177, "pytvH mSHHky mHSHb": 159, "Algvrytmym bbynh mlAKHvtyt": 133, "Algvrytmym KHlKHlyym": 111, "ptrvn b`yvt bAmTS`vt HypvSH": 88, "dHyst ntvnym byvm b 9:00": 66, "dHyst ntvnym byvm g 14:00": 44, "rvbvTym AvTvnvmyym": 22, "lmydh yySHvmyt brAyyh mmvHSHbt byvm d 15:00": 0, "lmydh yySHvmyt brAyyh mmvHSHbt byvm h 15:00": 0, "hskh sTTysTyt": 0, "nvSHAym mtkdmym brAyyh mmvHSHbt `m yySHvmym bhdmyh rpvAyt": 0, "SHyTvt lgylvy htkpvt syybr": 0, "nytvH myd` bmymdym gbvhym": 0, "gyAvmTryh bdydh": 0, "sybvKHyvt tkSHvrt": 0, "tAvryh SHl krypTvgrpyh": 0, "spykvt bvlyAnyt": 0, "prTyvt HySHvb": 0, "mbvA lkrypTvgrpyh": 0, "tKHnvt Algvrytmym mHkryym": 0, "nvSHAym mtkdmym btvrt hgrpym": 0}, "s85": {"dHyst ntvnym byvm b 9:00": 124, "dHyst ntvnym byvm g 14:00": 0, "ptrvn b`yvt bAmTS`vt HypvSH": 0, "Algvrytmym KHlKHlyym": 0, "lmydh yySHvmyt brAyyh mmvHSHbt byvm d 15:00": 0, "lmydh yySHvmyt brAyyh mmvHSHbt byvm h 15:00": 0, "rvbvTym AvTvnvmyym": 0, "hskh sTTysTyt": 0, "nvSHAym mtkdmym brAyyh mmvHSHbt `m yySHvmym bhdmyh rpvAyt": 0, "SHyTvt lgylvy htkpvt syybr": 0, "nytvH myd` bmymdym gbvhym": 0, "gyAvmTryh bdydh": 0, "lmydt mKHvnh": 393, "sybvKHyvt tkSHvrt": 0, "lmydh `mvkh v`ybvd SHpvt Tb`yvt": 0, "tAvryh SHl krypTvgrpyh": 209, "spykvt bvlyAnyt": 0, "Algvrytmym bbynh mlAKHvtyt": 119, "prTyvt HySHvb": 88, "mbvA lkrypTvgrpyh": 67, "pytvH mSHHky mHSHb": 0, "tKHnvt Algvrytmym mHkryym": 0, "nvSHAym mtkdmym btvrt hgrpym": 0}, "s87": {"dHyst ntvnym byvm b 9:00": 0, "dHyst ntvnym byvm g 14:00": 200, "ptrvn b`yvt bAmTS`vt HypvSH": 0, "Algvrytmym KHlKHlyym": 0, "lmydh yySHvmyt brAyyh mmvHSHbt byvm d 15:00": 0, "lmydh yySHvmyt brAyyh mmvHSHbt byvm h 15:00": 0, "rvbvTym AvTvnvmyym": 0, "hskh sTTysTyt": 0, "nvSHAym mtkdmym brAyyh mmvHSHbt `m yySHvmym bhdmyh rpvAyt": 0, "SHyTvt lgylvy htkpvt syybr": 206, "nytvH myd` bmymdym gbvhym": 78, "gyAvmTryh bdydh": 0, "lmydt mKHvnh": 0, "sybvKHyvt tkSHvrt": 137, "lmydh `mvkh v`ybvd SHpvt Tb`yvt": 0, "tAvryh SHl krypTvgrpyh": 96, "spykvt bvlyAnyt": 0, "Algvrytmym bbynh mlAKHvtyt": 0, "prTyvt HySHvb": 0, "mbvA lkrypTvgrpyh": 0, "pytvH mSHHky mHSHb": 212, "tKHnvt Algvrytmym mHkryym": 71, "nvSHAym mtkdmym btvrt hgrpym": 0}, "s88": {"dHyst ntvnym byvm b 9:00": 502, "dHyst ntvnym byvm g 14:00": 0, "lmydt mKHvnh": 498, "ptrvn b`yvt bAmTS`vt HypvSH": 0, "Algvrytmym KHlKHlyym": 0, "lmydh yySHvmyt brAyyh mmvHSHbt byvm d 15:00": 0, "lmydh yySHvmyt brAyyh mmvHSHbt byvm h 15:00": 0, "hskh sTTysTyt": 0, "rvbvTym AvTvnvmyym": 0, "nvSHAym mtkdmym brAyyh mmvHSHbt `m yySHvmym bhdmyh rpvAyt": 0, "SHyTvt lgylvy htkpvt syybr": 0, "nytvH myd` bmymdym gbvhym": 0, "gyAvmTryh bdydh": 0, "sybvKHyvt tkSHvrt": 0, "tAvryh SHl krypTvgrpyh": 0, "lmydh `mvkh v`ybvd SHpvt Tb`yvt": 0, "spykvt bvlyAnyt": 0, "Algvrytmym bbynh mlAKHvtyt": 0, "prTyvt HySHvb": 0, "mbvA lkrypTvgrpyh": 0, "pytvH mSHHky mHSHb": 0, "tKHnvt Algvrytmym mHkryym": 0, "nvSHAym mtkdmym btvrt hgrpym": 0}, "s90": {"Algvrytmym KHlKHlyym": 149, "hskh sTTysTyt": 111, "dHyst ntvnym byvm g 14:00": 90, "dHyst ntvnym byvm b 9:00": 111, "SHyTvt lgylvy htkpvt syybr": 90, "nytvH myd` bmymdym gbvhym": 90, "ptrvn b`yvt bAmTS`vt HypvSH": 90, "lmydt mKHvnh": 90, "lmydh `mvkh v`ybvd SHpvt Tb`yvt": 31, "pytvH mSHHky mHSHb": 0, "nvSHAym mtkdmym btvrt hgrpym": 0, "lmydh yySHvmyt brAyyh mmvHSHbt byvm d 15:00": 0, "lmydh yySHvmyt brAyyh mmvHSHbt byvm h 15:00": 0, "rvbvTym AvTvnvmyym": 0, "nvSHAym mtkdmym brAyyh mmvHSHbt `m yySHvmym bhdmyh rpvAyt": 0, "gyAvmTryh bdydh": 90, "sybvKHyvt tkSHvrt": 0, "tAvryh SHl krypTvgrpyh": 0, "spykvt bvlyAnyt": 0, "Algvrytmym bbynh mlAKHvtyt": 0, "prTyvt HySHvb": 0, "mbvA lkrypTvgrpyh": 0, "tKHnvt Algvrytmym mHkryym": 58}, "s91": {"dHyst ntvnym byvm b 9:00": 0, "dHyst ntvnym byvm g 14:00": 42, "ptrvn b`yvt bAmTS`vt HypvSH": 0, "Algvrytmym KHlKHlyym": 0, "lmydh yySHvmyt brAyyh mmvHSHbt byvm d 15:00": 0, "lmydh yySHvmyt brAyyh mmvHSHbt byvm h 15:00": 0, "rvbvTym AvTvnvmyym": 0, "hskh sTTysTyt": 271, "nvSHAym mtkdmym brAyyh mmvHSHbt `m yySHvmym bhdmyh rpvAyt": 0, "SHyTvt lgylvy htkpvt syybr": 301, "nytvH myd` bmymdym gbvhym": 386, "gyAvmTryh bdydh": 0, "lmydt mKHvnh": 0, "sybvKHyvt tkSHvrt": 0, "lmydh `mvkh v`ybvd SHpvt Tb`yvt": 0, "tAvryh SHl krypTvgrpyh": 0, "spykvt bvlyAnyt": 0, "Algvrytmym bbynh mlAKHvtyt": 0, "prTyvt HySHvb": 0, "mbvA lkrypTvgrpyh": 0, "pytvH mSHHky mHSHb": 0, "tKHnvt Algvrytmym mHkryym": 0, "nvSHAym mtkdmym btvrt hgrpym": 0}, "s96": {"dHyst ntvnym byvm b 9:00": 0, "dHyst ntvnym byvm g 14:00": 200, "ptrvn b`yvt bAmTS`vt HypvSH": 0, "Algvrytmym KHlKHlyym": 0, "lmydh yySHvmyt brAyyh mmvHSHbt byvm d 15:00": 0, "lmydh yySHvmyt brAyyh mmvHSHbt byvm h 15:00": 0, "rvbvTym AvTvnvmyym": 0, "hskh sTTysTyt": 0, "nvSHAym mtkdmym brAyyh mmvHSHbt `m yySHvmym bhdmyh rpvAyt": 0, "SHyTvt lgylvy htkpvt syybr": 100, "nytvH myd` bmymdym gbvhym": 0, "gyAvmTryh bdydh": 0, "lmydt mKHvnh": 500, "sybvKHyvt tkSHvrt": 100, "lmydh `mvkh v`ybvd SHpvt Tb`yvt": 100, "tAvryh SHl krypTvgrpyh": 0, "spykvt bvlyAnyt": 0, "Algvrytmym bbynh mlAKHvtyt": 0, "prTyvt HySHvb": 0, "mbvA lkrypTvgrpyh": 0, "pytvH mSHHky mHSHb": 0, "tKHnvt Algvrytmym mHkryym": 0, "nvSHAym mtkdmym btvrt hgrpym": 0}, "s100": {"dHyst ntvnym byvm b 9:00": 171, "dHyst ntvnym byvm g 14:00": 151, "SHyTvt lgylvy htkpvt syybr": 136, "nytvH myd` bmymdym gbvhym": 121, "lmydt mKHvnh": 106, "Algvrytmym KHlKHlyym": 90, "lmydh yySHvmyt brAyyh mmvHSHbt byvm d 15:00": 0, "ptrvn b`yvt bAmTS`vt HypvSH": 0, "lmydh yySHvmyt brAyyh mmvHSHbt byvm h 15:00": 0, "rvbvTym AvTvnvmyym": 75, "hskh sTTysTyt": 60, "nvSHAym mtkdmym brAyyh mmvHSHbt `m yySHvmym bhdmyh rpvAyt": 0, "gyAvmTryh bdydh": 0, "sybvKHyvt tkSHvrt": 0, "lmydh `mvkh v`ybvd SHpvt Tb`yvt": 0, "spykvt bvlyAnyt": 0, "Algvrytmym bbynh mlAKHvtyt": 0, "prTyvt HySHvb": 45, "mbvA lkrypTvgrpyh": 30, "tAvryh SHl krypTvgrpyh": 15, "pytvH mSHHky mHSHb": 0, "tKHnvt Algvrytmym mHkryym": 0, "nvSHAym mtkdmym btvrt hgrpym": 0}, "s101": {"dHyst ntvnym byvm b 9:00": 138, "dHyst ntvnym byvm g 14:00": 0, "ptrvn b`yvt bAmTS`vt HypvSH": 0, "Algvrytmym KHlKHlyym": 0, "lmydh yySHvmyt brAyyh mmvHSHbt byvm d 15:00": 0, "lmydh yySHvmyt brAyyh mmvHSHbt byvm h 15:00": 0, "rvbvTym AvTvnvmyym": 0, "hskh sTTysTyt": 33, "nvSHAym mtkdmym brAyyh mmvHSHbt `m yySHvmym bhdmyh rpvAyt": 0, "SHyTvt lgylvy htkpvt syybr": 0, "nytvH myd` bmymdym gbvhym": 15, "gyAvmTryh bdydh": 0, "lmydt mKHvnh": 478, "sybvKHyvt tkSHvrt": 120, "lmydh `mvkh v`ybvd SHpvt Tb`yvt": 105, "tAvryh SHl krypTvgrpyh": 0, "spykvt bvlyAnyt": 0, "Algvrytmym bbynh mlAKHvtyt": 0, "prTyvt HySHvb": 13, "mbvA lkrypTvgrpyh": 88, "pytvH mSHHky mHSHb": 0, "tKHnvt Algvrytmym mHkryym": 10, "nvSHAym mtkdmym btvrt hgrpym": 0}, "s106": {"dHyst ntvnym byvm b 9:00": 502, "dHyst ntvnym byvm g 14:00": 0, "ptrvn b`yvt bAmTS`vt HypvSH": 0, "Algvrytmym KHlKHlyym": 0, "lmydh yySHvmyt brAyyh mmvHSHbt byvm d 15:00": 0, "lmydh yySHvmyt brAyyh mmvHSHbt byvm h 15:00": 498, "rvbvTym AvTvnvmyym": 0, "hskh sTTysTyt": 0, "nvSHAym mtkdmym brAyyh mmvHSHbt `m yySHvmym bhdmyh rpvAyt": 0, "SHyTvt lgylvy htkpvt syybr": 0, "nytvH myd` bmymdym gbvhym": 0, "gyAvmTryh bdydh": 0, "lmydt mKHvnh": 0, "sybvKHyvt tkSHvrt": 0, "lmydh `mvkh v`ybvd SHpvt Tb`yvt": 0, "tAvryh SHl krypTvgrpyh": 0, "spykvt bvlyAnyt": 0, "Algvrytmym bbynh mlAKHvtyt": 0, "prTyvt HySHvb": 0, "mbvA lkrypTvgrpyh": 0, "pytvH mSHHky mHSHb": 0, "tKHnvt Algvrytmym mHkryym": 0, "nvSHAym mtkdmym btvrt hgrpym": 0}, "s108": {"dHyst ntvnym byvm b 9:00": 322, "dHyst ntvnym byvm g 14:00": 0, "ptrvn b`yvt bAmTS`vt HypvSH": 0, "Algvrytmym KHlKHlyym": 145, "lmydh yySHvmyt brAyyh mmvHSHbt byvm d 15:00": 0, "lmydh yySHvmyt brAyyh mmvHSHbt byvm h 15:00": 0, "rvbvTym AvTvnvmyym": 0, "hskh sTTysTyt": 184, "nvSHAym mtkdmym brAyyh mmvHSHbt `m yySHvmym bhdmyh rpvAyt": 0, "SHyTvt lgylvy htkpvt syybr": 180, "nytvH myd` bmymdym gbvhym": 0, "gyAvmTryh bdydh": 0, "lmydt mKHvnh": 0, "sybvKHyvt tkSHvrt": 0, "lmydh `mvkh v`ybvd SHpvt Tb`yvt": 0, "tAvryh SHl krypTvgrpyh": 0, "spykvt bvlyAnyt": 67, "Algvrytmym bbynh mlAKHvtyt": 0, "prTyvt HySHvb": 102, "mbvA lkrypTvgrpyh": 0, "pytvH mSHHky mHSHb": 0, "tKHnvt Algvrytmym mHkryym": 0, "nvSHAym mtkdmym btvrt hgrpym": 0}, "s109": {"pytvH mSHHky mHSHb": 175, "lmydh yySHvmyt brAyyh mmvHSHbt byvm h 15:00": 175, "hskh sTTysTyt": 172, "Algvrytmym KHlKHlyym": 150, "dHyst ntvnym byvm g 14:00": 0, "ptrvn b`yvt bAmTS`vt HypvSH": 0, "lmydh yySHvmyt brAyyh mmvHSHbt byvm d 15:00": 0, "rvbvTym AvTvnvmyym": 0, "dHyst ntvnym byvm b 9:00": 0, "SHyTvt lgylvy htkpvt syybr": 0, "nvSHAym mtkdmym brAyyh mmvHSHbt `m yySHvmym bhdmyh rpvAyt": 178, "nytvH myd` bmymdym gbvhym": 150, "gyAvmTryh bdydh": 0, "lmydt mKHvnh": 0, "lmydh `mvkh v`ybvd SHpvt Tb`yvt": 0, "sybvKHyvt tkSHvrt": 0, "tAvryh SHl krypTvgrpyh": 0, "Algvrytmym bbynh mlAKHvtyt": 0, "spykvt bvlyAnyt": 0, "prTyvt HySHvb": 0, "mbvA lkrypTvgrpyh": 0, "tKHnvt Algvrytmym mHkryym": 0, "nvSHAym mtkdmym btvrt hgrpym": 0}, "s110": {"dHyst ntvnym byvm g 14:00": 244, "dHyst ntvnym byvm b 9:00": 74, "SHyTvt lgylvy htkpvt syybr": 230, "lmydh `mvkh v`ybvd SHpvt Tb`yvt": 243, "lmydt mKHvnh": 145, "nytvH myd` bmymdym gbvhym": 0, "prTyvt HySHvb": 64, "Algvrytmym KHlKHlyym": 0, "tKHnvt Algvrytmym mHkryym": 0, "ptrvn b`yvt bAmTS`vt HypvSH": 0, "hskh sTTysTyt": 0, "gyAvmTryh bdydh": 0, "lmydh yySHvmyt brAyyh mmvHSHbt byvm d 15:00": 0, "lmydh yySHvmyt brAyyh mmvHSHbt byvm h 15:00": 0, "rvbvTym AvTvnvmyym": 0, "nvSHAym mtkdmym brAyyh mmvHSHbt `m yySHvmym bhdmyh rpvAyt": 0, "sybvKHyvt tkSHvrt": 0, "tAvryh SHl krypTvgrpyh": 0, "Algvrytmym bbynh mlAKHvtyt": 0, "spykvt bvlyAnyt": 0, "mbvA lkrypTvgrpyh": 0, "pytvH mSHHky mHSHb": 0, "nvSHAym mtkdmym btvrt hgrpym": 0}, "s111": {"dHyst ntvnym byvm b 9:00": 157, "dHyst ntvnym byvm g 14:00": 139, "ptrvn b`yvt bAmTS`vt HypvSH": 0, "Algvrytmym KHlKHlyym": 0, "lmydh yySHvmyt brAyyh mmvHSHbt byvm d 15:00": 0, "lmydh yySHvmyt brAyyh mmvHSHbt byvm h 15:00": 0, "rvbvTym AvTvnvmyym": 165, "hskh sTTysTyt": 132, "nvSHAym mtkdmym brAyyh mmvHSHbt `m yySHvmym bhdmyh rpvAyt": 0, "SHyTvt lgylvy htkpvt syybr": 407, "nytvH myd` bmymdym gbvhym": 0, "gyAvmTryh bdydh": 0, "lmydt mKHvnh": 0, "sybvKHyvt tkSHvrt": 0, "lmydh `mvkh v`ybvd SHpvt Tb`yvt": 0, "tAvryh SHl krypTvgrpyh": 0, "spykvt bvlyAnyt": 0, "Algvrytmym bbynh mlAKHvtyt": 0, "prTyvt HySHvb": 0, "mbvA lkrypTvgrpyh": 0, "pytvH mSHHky mHSHb": 0, "tKHnvt Algvrytmym mHkryym": 0, "nvSHAym mtkdmym btvrt hgrpym": 0}, "s112": {"dHyst ntvnym byvm b 9:00": 120, "dHyst ntvnym byvm g 14:00": 92, "ptrvn b`yvt bAmTS`vt HypvSH": 0, "Algvrytmym KHlKHlyym": 0, "lmydh yySHvmyt brAyyh mmvHSHbt byvm d 15:00": 0, "lmydh yySHvmyt brAyyh mmvHSHbt byvm h 15:00": 0, "rvbvTym AvTvnvmyym": 0, "hskh sTTysTyt": 320, "nvSHAym mtkdmym brAyyh mmvHSHbt `m yySHvmym bhdmyh rpvAyt": 0, "SHyTvt lgylvy htkpvt syybr": 356, "nytvH myd` bmymdym gbvhym": 0, "gyAvmTryh bdydh": 0, "lmydt mKHvnh": 112, "sybvKHyvt tkSHvrt": 0, "lmydh `mvkh v`ybvd SHpvt Tb`yvt": 0, "tAvryh SHl krypTvgrpyh": 0, "spykvt bvlyAnyt": 0, "Algvrytmym bbynh mlAKHvtyt": 0, "prTyvt HySHvb": 0, "mbvA lkrypTvgrpyh": 0, "pytvH mSHHky mHSHb": 0, "tKHnvt Algvrytmym mHkryym": 0, "nvSHAym mtkdmym btvrt hgrpym": 0}, "s113": {"dHyst ntvnym byvm b 9:00": 200, "dHyst ntvnym byvm g 14:00": 200, "ptrvn b`yvt bAmTS`vt HypvSH": 100, "Algvrytmym KHlKHlyym": 160, "lmydh yySHvmyt brAyyh mmvHSHbt byvm d 15:00": 0, "lmydh yySHvmyt brAyyh mmvHSHbt byvm h 15:00": 0, "rvbvTym AvTvnvmyym": 0, "hskh sTTysTyt": 200, "nvSHAym mtkdmym brAyyh mmvHSHbt `m yySHvmym bhdmyh rpvAyt": 0, "SHyTvt lgylvy htkpvt syybr": 0, "nytvH myd` bmymdym gbvhym": 40, "gyAvmTryh bdydh": 0, "lmydt mKHvnh": 100, "sybvKHyvt tkSHvrt": 0, "lmydh `mvkh v`ybvd SHpvt Tb`yvt": 0, "tAvryh SHl krypTvgrpyh": 0, "spykvt bvlyAnyt": 0, "Algvrytmym bbynh mlAKHvtyt": 0, "prTyvt HySHvb": 0, "mbvA lkrypTvgrpyh": 0, "pytvH mSHHky mHSHb": 0, "tKHnvt Algvrytmym mHkryym": 0, "nvSHAym mtkdmym btvrt hgrpym": 0}}, "agent_capacities": {"s64": 6, "s67": 6, "s68": 4, "s69": 4, "s71": 6, "s76": 6, "s78": 6, "s80": 2, "s81": 6, "s83": 6, "s84": 6, "s85": 6, "s87": 2, "s88": 6, "s90": 5, "s91": 3, "s96": 6, "s100": 6, "s101": 6, "s106": 6, "s108": 6, "s109": 6, "s110": 3, "s111": 6, "s112": 4, "s113": 5}, "item_capacities": {"dHyst ntvnym byvm b 9:00": 126, "dHyst ntvnym byvm g 14:00": 40, "ptrvn b`yvt bAmTS`vt HypvSH": 82, "Algvrytmym KHlKHlyym": 44, "lmydh yySHvmyt brAyyh mmvHSHbt byvm d 15:00": 50, "lmydh yySHvmyt brAyyh mmvHSHbt byvm h 15:00": 50, "rvbvTym AvTvnvmyym": 69, "hskh sTTysTyt": 80, "nvSHAym mtkdmym brAyyh mmvHSHbt `m yySHvmym bhdmyh rpvAyt": 40, "SHyTvt lgylvy htkpvt syybr": 55, "nytvH myd` bmymdym gbvhym": 77, "gyAvmTryh bdydh": 67, "lmydt mKHvnh": 81, "sybvKHyvt tkSHvrt": 50, "lmydh `mvkh v`ybvd SHpvt Tb`yvt": 86, "tAvryh SHl krypTvgrpyh": 50, "spykvt bvlyAnyt": 40, "Algvrytmym bbynh mlAKHvtyt": 84, "prTyvt HySHvb": 65, "mbvA lkrypTvgrpyh": 50, "pytvH mSHHky mHSHb": 40, "tKHnvt Algvrytmym mHkryym": 41, "nvSHAym mtkdmym btvrt hgrpym": 40}, "agent_conflicts": {"s71": ["SHyTvt lgylvy htkpvt syybr", "gyAvmTryh bdydh", "nytvH myd` bmymdym gbvhym", "lmydh yySHvmyt brAyyh mmvHSHbt byvm h 15:00", "lmydh `mvkh v`ybvd SHpvt Tb`yvt", "spykvt bvlyAnyt", "mbvA lkrypTvgrpyh", "prTyvt HySHvb", "Algvrytmym bbynh mlAKHvtyt", "sybvKHyvt tkSHvrt", "tAvryh SHl krypTvgrpyh"], "s76": ["tAvryh SHl krypTvgrpyh", "gyAvmTryh bdydh", "nvSHAym mtkdmym brAyyh mmvHSHbt `m yySHvmym bhdmyh rpvAyt", "lmydt mKHvnh", "nytvH myd` bmymdym gbvhym", "lmydh yySHvmyt brAyyh mmvHSHbt byvm h 15:00", "lmydh yySHvmyt brAyyh mmvHSHbt byvm d 15:00", "lmydh `mvkh v`ybvd SHpvt Tb`yvt", "hskh sTTysTyt", "dHyst ntvnym byvm b 9:00", "spykvt bvlyAnyt", "mbvA lkrypTvgrpyh", "prTyvt HySHvb", "Algvrytmym bbynh mlAKHvtyt", "nvSHAym mtkdmym btvrt hgrpym", "Algvrytmym KHlKHlyym", "sybvKHyvt tkSHvrt", "ptrvn b`yvt bAmTS`vt HypvSH"], "s78": ["SHyTvt lgylvy htkpvt syybr", "dHyst ntvnym byvm g 14:00", "mbvA lkrypTvgrpyh", "tKHnvt Algvrytmym mHkryym", "nvSHAym mtkdmym btvrt hgrpym", "gyAvmTryh bdydh", "nytvH myd` bmymdym gbvhym", "dHyst ntvnym byvm b 9:00", "ptrvn b`yvt bAmTS`vt HypvSH", "lmydh yySHvmyt brAyyh mmvHSHbt byvm h 15:00", "lmydh yySHvmyt brAyyh mmvHSHbt byvm d 15:00", "hskh sTTysTyt", "spykvt bvlyAnyt", "prTyvt HySHvb", "nvSHAym mtkdmym brAyyh mmvHSHbt `m yySHvmym bhdmyh rpvAyt", "rvbvTym AvTvnvmyym", "pytvH mSHHky mHSHb", "Algvrytmym bbynh mlAKHvtyt", "Algvrytmym KHlKHlyym", "sybvKHyvt tkSHvrt", "tAvryh SHl krypTvgrpyh"], "s80": ["rvbvTym AvTvnvmyym", "tAvryh SHl krypTvgrpyh", "SHyTvt lgylvy htkpvt syybr", "gyAvmTryh bdydh", "lmydt mKHvnh", "lmydh yySHvmyt brAyyh mmvHSHbt byvm h 15:00", "pytvH mSHHky mHSHb", "lmydh `mvkh v`ybvd SHpvt Tb`yvt", "tKHnvt Algvrytmym mHkryym", "spykvt bvlyAnyt", "mbvA lkrypTvgrpyh", "prTyvt HySHvb", "Algvrytmym bbynh mlAKHvtyt", "nvSHAym mtkdmym btvrt hgrpym", "sybvKHyvt tkSHvrt", "ptrvn b`yvt bAmTS`vt HypvSH"], "s81": ["rvbvTym AvTvnvmyym", "tAvryh SHl krypTvgrpyh", "nvSHAym mtkdmym brAyyh mmvHSHbt `m yySHvmym bhdmyh rpvAyt", "nytvH myd` bmymdym gbvhym", "lmydh yySHvmyt brAyyh mmvHSHbt byvm h 15:00", "lmydh yySHvmyt brAyyh mmvHSHbt byvm d 15:00", "lmydh `mvkh v`ybvd SHpvt Tb`yvt", "hskh sTTysTyt", "spykvt bvlyAnyt", "tKHnvt Algvrytmym mHkryym", "mbvA lkrypTvgrpyh", "prTyvt HySHvb", "Algvrytmym bbynh mlAKHvtyt", "nvSHAym mtkdmym btvrt hgrpym", "Algvrytmym KHlKHlyym", "sybvKHyvt tkSHvrt", "ptrvn b`yvt bAmTS`vt HypvSH"], "s83": ["rvbvTym AvTvnvmyym", "SHyTvt lgylvy htkpvt syybr", "gyAvmTryh bdydh", "nytvH myd` bmymdym gbvhym", "pytvH mSHHky mHSHb", "hskh sTTysTyt", "spykvt bvlyAnyt", "mbvA lkrypTvgrpyh", "prTyvt HySHvb", "tKHnvt Algvrytmym mHkryym", "Algvrytmym KHlKHlyym", "nvSHAym mtkdmym btvrt hgrpym", "tAvryh SHl krypTvgrpyh"], "s84": ["tAvryh SHl krypTvgrpyh", "SHyTvt lgylvy htkpvt syybr", "gyAvmTryh bdydh", "nytvH myd` bmymdym gbvhym", "lmydh yySHvmyt brAyyh mmvHSHbt byvm h 15:00", "lmydh yySHvmyt brAyyh mmvHSHbt byvm d 15:00", "hskh sTTysTyt", "spykvt bvlyAnyt", "mbvA lkrypTvgrpyh", "prTyvt HySHvb", "tKHnvt Algvrytmym mHkryym", "nvSHAym mtkdmym btvrt hgrpym", "sybvKHyvt tkSHvrt", "nvSHAym mtkdmym brAyyh mmvHSHbt `m yySHvmym bhdmyh rpvAyt"], "s85": ["rvbvTym AvTvnvmyym", "SHyTvt lgylvy htkpvt syybr", "gyAvmTryh bdydh", "nvSHAym mtkdmym brAyyh mmvHSHbt `m yySHvmym bhdmyh rpvAyt", "dHyst ntvnym byvm g 14:00", "nytvH myd` bmymdym gbvhym", "lmydh yySHvmyt brAyyh mmvHSHbt byvm h 15:00", "pytvH mSHHky mHSHb", "lmydh yySHvmyt brAyyh mmvHSHbt byvm d 15:00", "lmydh `mvkh v`ybvd SHpvt Tb`yvt", "hskh sTTysTyt", "spykvt bvlyAnyt", "tKHnvt Algvrytmym mHkryym", "nvSHAym mtkdmym btvrt hgrpym", "Algvrytmym KHlKHlyym", "sybvKHyvt tkSHvrt", "ptrvn b`yvt bAmTS`vt HypvSH"], "s87": ["rvbvTym AvTvnvmyym", "gyAvmTryh bdydh", "nvSHAym mtkdmym brAyyh mmvHSHbt `m yySHvmym bhdmyh rpvAyt", "lmydt mKHvnh", "lmydh yySHvmyt brAyyh mmvHSHbt byvm h 15:00", "lmydh yySHvmyt brAyyh mmvHSHbt byvm d 15:00", "lmydh `mvkh v`ybvd SHpvt Tb`yvt", "hskh sTTysTyt", "dHyst ntvnym byvm b 9:00", "spykvt bvlyAnyt", "mbvA lkrypTvgrpyh", "prTyvt HySHvb", "Algvrytmym bbynh mlAKHvtyt", "Algvrytmym KHlKHlyym", "nvSHAym mtkdmym btvrt hgrpym", "ptrvn b`yvt bAmTS`vt HypvSH"], "s88": ["SHyTvt lgylvy htkpvt syybr", "mbvA lkrypTvgrpyh", "tKHnvt Algvrytmym mHkryym", "nvSHAym mtkdmym btvrt hgrpym", "gyAvmTryh bdydh", "nytvH myd` bmymdym gbvhym", "lmydh `mvkh v`ybvd SHpvt Tb`yvt", "ptrvn b`yvt bAmTS`vt HypvSH", "lmydh yySHvmyt brAyyh mmvHSHbt byvm h 15:00", "lmydh yySHvmyt brAyyh mmvHSHbt byvm d 15:00", "hskh sTTysTyt", "spykvt bvlyAnyt", "prTyvt HySHvb", "nvSHAym mtkdmym brAyyh mmvHSHbt `m yySHvmym bhdmyh rpvAyt", "rvbvTym AvTvnvmyym", "pytvH mSHHky mHSHb", "Algvrytmym bbynh mlAKHvtyt", "Algvrytmym KHlKHlyym", "sybvKHyvt tkSHvrt", "tAvryh SHl krypTvgrpyh"], "s90": ["rvbvTym AvTvnvmyym", "tAvryh SHl krypTvgrpyh", "lmydh yySHvmyt brAyyh mmvHSHbt byvm h 15:00", "lmydh yySHvmyt brAyyh mmvHSHbt byvm d 15:00", "spykvt bvlyAnyt", "mbvA lkrypTvgrpyh", "prTyvt HySHvb", "Algvrytmym bbynh mlAKHvtyt", "sybvKHyvt tkSHvrt", "nvSHAym mtkdmym brAyyh mmvHSHbt `m yySHvmym bhdmyh rpvAyt"], "s96": ["rvbvTym AvTvnvmyym", "gyAvmTryh bdydh", "nytvH myd` bmymdym gbvhym", "hskh sTTysTyt", "dHyst ntvnym byvm b 9:00", "spykvt bvlyAnyt", "tKHnvt Algvrytmym mHkryym", "Algvrytmym KHlKHlyym", "nvSHAym mtkdmym btvrt hgrpym", "tAvryh SHl krypTvgrpyh"], "s100": ["gyAvmTryh bdydh", "lmydh yySHvmyt brAyyh mmvHSHbt byvm h 15:00", "pytvH mSHHky mHSHb", "lmydh yySHvmyt brAyyh mmvHSHbt byvm d 15:00", "ptrvn b`yvt bAmTS`vt HypvSH", "lmydh `mvkh v`ybvd SHpvt Tb`yvt", "spykvt bvlyAnyt", "tKHnvt Algvrytmym mHkryym", "Algvrytmym bbynh mlAKHvtyt", "nvSHAym mtkdmym btvrt hgrpym", "sybvKHyvt tkSHvrt", "nvSHAym mtkdmym brAyyh mmvHSHbt `m yySHvmym bhdmyh rpvAyt"], "s101": ["lmydh yySHvmyt brAyyh mmvHSHbt byvm h 15:00", "lmydh yySHvmyt brAyyh mmvHSHbt byvm d 15:00", "spykvt bvlyAnyt", "nvSHAym mtkdmym btvrt hgrpym", "ptrvn b`yvt bAmTS`vt HypvSH"], "s108": ["rvbvTym AvTvnvmyym", "gyAvmTryh bdydh", "lmydh yySHvmyt brAyyh mmvHSHbt byvm h 15:00", "pytvH mSHHky mHSHb", "lmydh yySHvmyt brAyyh mmvHSHbt byvm d 15:00", "ptrvn b`yvt bAmTS`vt HypvSH", "lmydh `mvkh v`ybvd SHpvt Tb`yvt", "tKHnvt Algvrytmym mHkryym", "mbvA lkrypTvgrpyh", "Algvrytmym bbynh mlAKHvtyt", "nvSHAym mtkdmym btvrt hgrpym", "sybvKHyvt tkSHvrt", "nvSHAym mtkdmym brAyyh mmvHSHbt `m yySHvmym bhdmyh rpvAyt"], "s109": ["lmydh `mvkh v`ybvd SHpvt Tb`yvt", "nvSHAym mtkdmym btvrt hgrpym", "gyAvmTryh bdydh", "sybvKHyvt tkSHvrt"], "s110": ["rvbvTym AvTvnvmyym", "lmydh yySHvmyt brAyyh mmvHSHbt byvm h 15:00", "pytvH mSHHky mHSHb", "lmydh yySHvmyt brAyyh mmvHSHbt byvm d 15:00", "spykvt bvlyAnyt", "nvSHAym mtkdmym btvrt hgrpym", "nvSHAym mtkdmym brAyyh mmvHSHbt `m yySHvmym bhdmyh rpvAyt"], "s111": ["tAvryh SHl krypTvgrpyh", "gyAvmTryh bdydh", "lmydt mKHvnh", "nytvH myd` bmymdym gbvhym", "lmydh yySHvmyt brAyyh mmvHSHbt byvm h 15:00", "pytvH mSHHky mHSHb", "lmydh yySHvmyt brAyyh mmvHSHbt byvm d 15:00", "ptrvn b`yvt bAmTS`vt HypvSH", "lmydh `mvkh v`ybvd SHpvt Tb`yvt", "spykvt bvlyAnyt", "tKHnvt Algvrytmym mHkryym", "mbvA lkrypTvgrpyh", "prTyvt HySHvb", "Algvrytmym bbynh mlAKHvtyt", "nvSHAym mtkdmym btvrt hgrpym", "Algvrytmym KHlKHlyym", "sybvKHyvt tkSHvrt", "nvSHAym mtkdmym brAyyh mmvHSHbt `m yySHvmym bhdmyh rpvAyt"], "s112": ["tAvryh SHl krypTvgrpyh", "gyAvmTryh bdydh", "lmydh yySHvmyt brAyyh mmvHSHbt byvm h 15:00", "pytvH mSHHky mHSHb", "lmydh yySHvmyt brAyyh mmvHSHbt byvm d 15:00", "ptrvn b`yvt bAmTS`vt HypvSH", "lmydh `mvkh v`ybvd SHpvt Tb`yvt", "spykvt bvlyAnyt", "tKHnvt Algvrytmym mHkryym", "mbvA lkrypTvgrpyh", "prTyvt HySHvb", "Algvrytmym bbynh mlAKHvtyt", "nvSHAym mtkdmym btvrt hgrpym", "Algvrytmym KHlKHlyym", "sybvKHyvt tkSHvrt", "nvSHAym mtkdmym brAyyh mmvHSHbt `m yySHvmym bhdmyh rpvAyt"], "s113": ["rvbvTym AvTvnvmyym", "tAvryh SHl krypTvgrpyh", "gyAvmTryh bdydh", "lmydh yySHvmyt brAyyh mmvHSHbt byvm h 15:00", "pytvH mSHHky mHSHb", "lmydh yySHvmyt brAyyh mmvHSHbt byvm d 15:00", "lmydh `mvkh v`ybvd SHpvt Tb`yvt", "tKHnvt Algvrytmym mHkryym", "spykvt bvlyAnyt", "mbvA lkrypTvgrpyh", "Algvrytmym bbynh mlAKHvtyt", "nvSHAym mtkdmym btvrt hgrpym", "sybvKHyvt tkSHvrt", "nvSHAym mtkdmym brAyyh mmvHSHbt `m yySHvmym bhdmyh rpvAyt"]}, "item_conflicts": {"dHyst ntvnym byvm b 9:00": ["dHyst ntvnym byvm g 14:00", "nvSHAym mtkdmym btvrt hgrpym"], "dHyst ntvnym byvm g 14:00": ["dHyst ntvnym byvm b 9:00", "mbvA lkrypTvgrpyh"], "nvSHAym mtkdmym btvrt hgrpym": ["hskh sTTysTyt", "dHyst ntvnym byvm b 9:00"], "lmydh yySHvmyt brAyyh mmvHSHbt byvm d 15:00": ["lmydh yySHvmyt brAyyh mmvHSHbt byvm h 15:00"], "lmydh yySHvmyt brAyyh mmvHSHbt byvm h 15:00": ["lmydh yySHvmyt brAyyh mmvHSHbt byvm d 15:00"], "hskh sTTysTyt": ["nvSHAym mtkdmym btvrt hgrpym"], "SHyTvt lgylvy htkpvt syybr": ["lmydt mKHvnh"], "lmydt mKHvnh": ["SHyTvt lgylvy htkpvt syybr"], "mbvA lkrypTvgrpyh": ["dHyst ntvnym byvm g 14:00"]}}
    start_time = time.time()
    
    model = Model()
    
    #collect from data
    students = list(data["valuations"].keys())
    courses = list(data["item_capacities"].keys())
    
    x_vars = {}  
    I_vars = {}  
    for student in students:
        for course in courses:
            x_vars[(student, course)] = model.addVar(vtype=GRB.CONTINUOUS, 
                                                   name=f"x_{student}_{course}", 
                                                   lb=0, ub=1)
            I_vars[(student, course)] = model.addVar(vtype=GRB.BINARY, 
                                                   name=f"I_{student}_{course}")
    
    model.update()
    
    #student capacity constraints
    for student in students:
        expr = LinExpr()
        for course in courses:
            expr.addTerms(1, I_vars[(student, course)])
        model.addConstr(expr <= data["agent_capacities"][student])
        model.addConstr(quicksum(x_vars[(student, course)] for course in courses) >= 2)
    
    #course capacity constraints
    for course in courses:
        expr = LinExpr()
        for student in students:
            expr.addTerms(1, I_vars[(student, course)])
        model.addConstr(expr <= data["item_capacities"][course])
    
    #course conflict constraints
    for student in students:
        for course in item_conflicts:
            for conflicting_course in item_conflicts[course]:
                model.addConstr(I_vars[(student, course)] + 
                              I_vars[(student, conflicting_course)] <= 1)
    
    
    #envy-freeness constraints
    for student_a in students:
        for student_b in students:
            if student_a != student_b:
                utility_a = LinExpr()
                utility_b = LinExpr()
                for course in courses:
                    if course in data["valuations"][student_a]:
                        value_a = data["valuations"][student_a][course]
                        utility_a.addTerms(value_a, I_vars[(student_a, course)])
                        utility_b.addTerms(value_a, x_vars[(student_b, course)])
                        #utility_b.addTerms(value_a, I_vars[(student_b, course)])
                model.addConstr(utility_a >= utility_b)

    for student in students:
        utility_current = LinExpr()
        utility_unallocated = LinExpr()

        for course in courses:
            if course in data["valuations"][student]:
                value = data["valuations"][student][course]  
                #utility from current allocation
                utility_current.addTerms(value, I_vars[(student, course)])   
                #check if the course is unallocated
                unallocated_expr = LinExpr()
                for other_student in students:
                    if other_student != student:
                        unallocated_expr.addTerms(1, I_vars[(other_student, course)])                
                #define utility from unallocated courses
                unallocated_course_utility = value * (1 - unallocated_expr)                
                #sdd terms for unallocated utility
                utility_unallocated.add(unallocated_course_utility)
        #add the constraint: Current utility >= utility from unallocated allocations
        model.addConstr(utility_current >= utility_unallocated, name=f"envy_free_unallocated_{student}")

    
    #variable relationship constraints
    for student in students:
        for course in courses:
            model.addConstr(I_vars[(student, course)] >= x_vars[(student, course)])
    
    #maximize utility
    obj = LinExpr()
    for student in students:
        for course in courses:
            if course in data["valuations"][student]:
                value = data["valuations"][student][course]
                obj.addTerms(value, I_vars[(student, course)])
    
    model.setObjective(0, GRB.MAXIMIZE)
    
    
    model.optimize()
    end_time = time.time()
    
    #metrics
    runtime = end_time - start_time
    social_welfare = sum(data["valuations"][student].get(course, 0) * 
                        I_vars[(student, course)].X 
                        for student in students 
                        for course in courses
                        if course in data["valuations"][student])
    
    #print allocations
    allocations = {}
    print("\nAllocations and Utilities:")
    for student in students:
        allocations[student] = []
        student_utility = 0
        for course in courses:
            if I_vars[(student, course)].X > 0.5:
                if course in data["valuations"][student]:
                    utility = data["valuations"][student][course]
                    student_utility += utility
                    allocations[student].append(course)
                    print(f"{student} gets {course} (utility: {utility})")
        print(f"{student} total utility: {student_utility}\n")

    #check for EF violations
    ef_violations = 0
    violation_details = []
    for student_a in students:
        for student_b in students:
            if student_a != student_b:
                utility_a = sum(data["valuations"][student_a].get(course, 0) * 
                              I_vars[(student_a, course)].X 
                              for course in courses 
                              if course in data["valuations"][student_a])
                utility_b = sum(data["valuations"][student_a].get(course, 0) * 
                              I_vars[(student_b, course)].X 
                              for course in courses 
                              if course in data["valuations"][student_a])
                if utility_a < utility_b:
                    ef_violations += 1
                    violation_details.append({
                        'student_a': student_a,
                        'student_b': student_b,
                        'utility_a': utility_a,
                        'utility_b': utility_b
                    })
    
    #output
    print(f"\nRuntime: {runtime:.2f} seconds")
    print(f"Social Welfare: {social_welfare:.2f}")
    print(f"Number of EF violations: {ef_violations}")
    
    if ef_violations > 0:
        print("\nEF Violation Details:")
        for violation in violation_details:
            print(f"{violation['student_a']} envies {violation['student_b']}")
            print(f"  Own utility: {violation['utility_a']:.2f}")
            print(f"  Envied utility: {violation['utility_b']:.2f}")
    
    return {
        'runtime': runtime,
        'social_welfare': social_welfare,
        'ef_violations': ef_violations,
        'violation_details': violation_details,
        'allocations': allocations
    }


if __name__ == "__main__":
    results = solve_ef_allocation()


