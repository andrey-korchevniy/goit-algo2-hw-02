from typing import List, Dict
from dataclasses import dataclass

@dataclass
class PrintJob:
    id: str
    volume: float
    priority: int
    print_time: int

@dataclass
class PrinterConstraints:
    max_volume: float
    max_items: int

def optimize_printing(print_jobs: List[Dict], constraints: Dict) -> Dict:
    """
    Optimizes the 3D printing queue according to priorities and printer constraints
    Args:
        print_jobs: List of print jobs
        constraints: Printer constraints
    Returns:
        Dict with print order and total time
    """
    # Convert input dicts to dataclass objects
    jobs = [PrintJob(**job) for job in print_jobs]
    printer = PrinterConstraints(**constraints)

    # Sort jobs by priority (ascending: 1,2,3), then by id for stability
    jobs.sort(key=lambda x: (x.priority, x.id))

    print_order = []  # List of job ids in print order
    total_time = 0    # Total print time
    i = 0
    n = len(jobs)
    while i < n:
        batch = []  # Current batch of jobs
        batch_volume = 0.0
        batch_count = 0
        j = i
        # Try to fill the batch with as many jobs as possible within constraints
        while j < n:
            job = jobs[j]
            if (batch_volume + job.volume <= printer.max_volume) and (batch_count + 1 <= printer.max_items):
                batch.append(job)
                batch_volume += job.volume
                batch_count += 1
                j += 1
            else:
                break  # Constraints exceeded, finish current batch
        # If no job was added (single job too big), force add one job
        if not batch:
            batch.append(jobs[i])
            j = i + 1
        # Add job ids to print order
        print_order.extend([job.id for job in batch])
        # Batch time is the max print_time in the batch
        batch_time = max(job.print_time for job in batch)
        total_time += batch_time
        i = j  # Move to next jobs

    return {
        "print_order": print_order,
        "total_time": total_time
    }

# Тестування

def test_printing_optimization():
    # Test 1: Same priority models
    test1_jobs = [
        {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 1, "print_time": 150}
    ]

    # Test 2: Different priorities
    test2_jobs = [
        {"id": "M1", "volume": 100, "priority": 2, "print_time": 120},  # lab
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},   # diploma
        {"id": "M3", "volume": 120, "priority": 3, "print_time": 150}   # personal
    ]

    # Test 3: Exceeding volume constraints
    test3_jobs = [
        {"id": "M1", "volume": 250, "priority": 1, "print_time": 180},
        {"id": "M2", "volume": 200, "priority": 1, "print_time": 150},
        {"id": "M3", "volume": 180, "priority": 2, "print_time": 120}
    ]

    constraints = {
        "max_volume": 300,
        "max_items": 2
    }

    print("Тест 1 (однаковий пріоритет):")
    result1 = optimize_printing(test1_jobs, constraints)
    print(f"Порядок друку: {result1['print_order']}")
    print(f"Загальний час: {result1['total_time']} хвилин")

    print("\nТест 2 (різні пріоритети):")
    result2 = optimize_printing(test2_jobs, constraints)
    print(f"Порядок друку: {result2['print_order']}")
    print(f"Загальний час: {result2['total_time']} хвилин")

    print("\nТест 3 (перевищення обмежень):")
    result3 = optimize_printing(test3_jobs, constraints)
    print(f"Порядок друку: {result3['print_order']}")
    print(f"Загальний час: {result3['total_time']} хвилин")

if __name__ == "__main__":
    test_printing_optimization() 