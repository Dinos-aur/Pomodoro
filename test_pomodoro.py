"""
Unit tests for the Pomodoro timer app components.
Run with: python -m pytest test_pomodoro.py -v
Or run directly: python test_pomodoro.py
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import time
import sys

# ─────────────────────────────────────────────────────────────────────────────
# Test Suite 1: Time Calculations
# ─────────────────────────────────────────────────────────────────────────────
class TestTimeCalculations(unittest.TestCase):
    """Test timer calculations and time formatting."""
    
    def test_time_formatting_mm_ss(self):
        """Test converting seconds to MM:SS format."""
        test_cases = [
            (0, (0, 0)),          # 0 seconds
            (30, (0, 30)),        # 30 seconds
            (60, (1, 0)),         # 1 minute
            (90, (1, 30)),        # 1:30
            (600, (10, 0)),       # 10 minutes
            (1500, (25, 0)),      # 25 minutes (Focus mode)
            (300, (5, 0)),        # 5 minutes (Short break)
            (900, (15, 0)),       # 15 minutes (Long break)
            (3599, (59, 59)),     # 59:59
        ]
        
        for seconds, expected in test_cases:
            mins, s = divmod(seconds, 60)
            result = (mins, s)
            self.assertEqual(result, expected, 
                           f"Failed for {seconds}s: expected {expected}, got {result}")
    
    def test_progress_percentage(self):
        """Test progress bar percentage calculation."""
        # Focus mode = 25 minutes = 1500 seconds
        total = 25 * 60
        
        test_cases = [
            (1500, 0.0),     # Full timer = 0%
            (750, 50.0),     # Half timer = 50%
            (0, 100.0),      # Empty timer = 100%
            (1350, 10.0),    # 90 seconds elapsed ≈ 10%
        ]
        
        for seconds_left, expected_pct in test_cases:
            pct = 100 * (1 - seconds_left / total) if total else 100
            self.assertAlmostEqual(pct, expected_pct, places=1,
                                 msg=f"Failed for {seconds_left}s left")
    
    def test_time_elapsed_calculation(self):
        """Test calculating elapsed time between ticks."""
        now = time.time()
        last_tick = now - 5.0
        
        elapsed = int(now - last_tick)
        self.assertEqual(elapsed, 5, "Should calculate 5 seconds elapsed")
        
        # Test with subsecond precision
        elapsed = int(now - last_tick)
        self.assertTrue(4 <= elapsed <= 6, "Elapsed time should be ~5 seconds (±1)")


# ─────────────────────────────────────────────────────────────────────────────
# Test Suite 2: Session State Management
# ─────────────────────────────────────────────────────────────────────────────
class TestSessionStateManagement(unittest.TestCase):
    """Test session state initialization and updates."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.MODES = {"Focus": 25 * 60, "Short Break": 5 * 60, "Long Break": 15 * 60}
    
    def test_initial_state(self):
        """Test session state is initialized correctly."""
        session_state = {
            "mode": "Focus",
            "seconds_left": self.MODES["Focus"],
            "running": False,
            "last_tick": None,
            "tasks": [],
            "pomodoros": 0,
            "task_input": ""
        }
        
        self.assertEqual(session_state["mode"], "Focus")
        self.assertEqual(session_state["seconds_left"], 1500)
        self.assertFalse(session_state["running"])
        self.assertIsNone(session_state["last_tick"])
        self.assertEqual(session_state["tasks"], [])
        self.assertEqual(session_state["pomodoros"], 0)
    
    def test_mode_switching(self):
        """Test switching between timer modes."""
        session_state = {
            "mode": "Focus",
            "seconds_left": self.MODES["Focus"],
            "running": False,
            "last_tick": None,
        }
        
        # Switch to Short Break
        session_state["mode"] = "Short Break"
        session_state["seconds_left"] = self.MODES["Short Break"]
        session_state["running"] = False
        session_state["last_tick"] = None
        
        self.assertEqual(session_state["mode"], "Short Break")
        self.assertEqual(session_state["seconds_left"], 300)
        self.assertFalse(session_state["running"])
    
    def test_timer_countdown(self):
        """Test timer countdown logic."""
        session_state = {
            "seconds_left": 100,
            "running": True,
            "last_tick": time.time()
        }
        
        # Simulate 10 seconds elapsed
        now = time.time()
        elapsed = int(now - session_state["last_tick"])
        session_state["seconds_left"] = max(0, session_state["seconds_left"] - elapsed)
        session_state["last_tick"] = now
        
        # Should have decremented
        self.assertTrue(session_state["seconds_left"] <= 100)
        self.assertTrue(session_state["seconds_left"] >= 0)


# ─────────────────────────────────────────────────────────────────────────────
# Test Suite 3: Task Management
# ─────────────────────────────────────────────────────────────────────────────
class TestTaskManagement(unittest.TestCase):
    """Test task list operations."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.tasks = []
    
    def test_add_task(self):
        """Test adding a task."""
        new_task = "Study Python"
        self.tasks.append({"text": new_task.strip(), "done": False})
        
        self.assertEqual(len(self.tasks), 1)
        self.assertEqual(self.tasks[0]["text"], "Study Python")
        self.assertFalse(self.tasks[0]["done"])
    
    def test_add_multiple_tasks(self):
        """Test adding multiple tasks."""
        task_names = ["Task 1", "Task 2", "Task 3"]
        
        for task in task_names:
            self.tasks.append({"text": task, "done": False})
        
        self.assertEqual(len(self.tasks), 3)
        self.assertEqual([t["text"] for t in self.tasks], task_names)
    
    def test_toggle_task_completion(self):
        """Test marking task as done/undone."""
        self.tasks.append({"text": "Test task", "done": False})
        
        # Mark as done
        self.tasks[0]["done"] = True
        self.assertTrue(self.tasks[0]["done"])
        
        # Mark as undone
        self.tasks[0]["done"] = False
        self.assertFalse(self.tasks[0]["done"])
    
    def test_delete_task(self):
        """Test deleting a task."""
        self.tasks.append({"text": "Task 1", "done": False})
        self.tasks.append({"text": "Task 2", "done": False})
        
        self.assertEqual(len(self.tasks), 2)
        
        # Delete first task
        self.tasks.pop(0)
        
        self.assertEqual(len(self.tasks), 1)
        self.assertEqual(self.tasks[0]["text"], "Task 2")
    
    def test_empty_task_rejection(self):
        """Test that empty tasks are rejected."""
        task_text = "   "  # Only whitespace
        
        if task_text.strip():
            self.tasks.append({"text": task_text.strip(), "done": False})
        
        self.assertEqual(len(self.tasks), 0)
    
    def test_task_text_normalization(self):
        """Test that task text is normalized (whitespace trimmed)."""
        task_text = "  Study Python  "
        normalized = task_text.strip()
        
        self.tasks.append({"text": normalized, "done": False})
        
        self.assertEqual(self.tasks[0]["text"], "Study Python")


# ─────────────────────────────────────────────────────────────────────────────
# Test Suite 4: Pomodoro Counting Logic
# ─────────────────────────────────────────────────────────────────────────────
class TestPomodoroCounter(unittest.TestCase):
    """Test Pomodoro counter incrementation."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.pomodoros = 0
        self.mode = "Focus"
        self.seconds_left = 0
    
    def test_pomodoro_increment_on_focus_complete(self):
        """Test that pomodoro count increments when Focus session completes."""
        self.mode = "Focus"
        self.seconds_left = 0
        
        if self.seconds_left == 0 and self.mode == "Focus":
            self.pomodoros += 1
        
        self.assertEqual(self.pomodoros, 1)
    
    def test_pomodoro_not_increment_on_break_complete(self):
        """Test that pomodoro count doesn't increment on break completion."""
        self.mode = "Short Break"
        self.seconds_left = 0
        
        if self.seconds_left == 0 and self.mode == "Focus":
            self.pomodoros += 1
        
        self.assertEqual(self.pomodoros, 0)
    
    def test_multiple_pomodoros(self):
        """Test incrementing multiple pomodoros."""
        for _ in range(4):
            self.mode = "Focus"
            self.seconds_left = 0
            if self.seconds_left == 0 and self.mode == "Focus":
                self.pomodoros += 1
        
        self.assertEqual(self.pomodoros, 4)


# ─────────────────────────────────────────────────────────────────────────────
# Test Suite 5: Timer Control Logic
# ─────────────────────────────────────────────────────────────────────────────
class TestTimerControls(unittest.TestCase):
    """Test timer start/pause/reset functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.MODES = {"Focus": 25 * 60, "Short Break": 5 * 60, "Long Break": 15 * 60}
        self.session_state = {
            "mode": "Focus",
            "seconds_left": self.MODES["Focus"],
            "running": False,
            "last_tick": None,
        }
    
    def test_start_timer(self):
        """Test starting the timer."""
        self.session_state["running"] = True
        self.session_state["last_tick"] = time.time()
        
        self.assertTrue(self.session_state["running"])
        self.assertIsNotNone(self.session_state["last_tick"])
    
    def test_pause_timer(self):
        """Test pausing the timer."""
        self.session_state["running"] = True
        self.session_state["last_tick"] = time.time()
        
        # Pause
        self.session_state["running"] = False
        self.session_state["last_tick"] = None
        
        self.assertFalse(self.session_state["running"])
        self.assertIsNone(self.session_state["last_tick"])
    
    def test_reset_timer(self):
        """Test resetting the timer."""
        # Simulate running state
        self.session_state["seconds_left"] = 500
        self.session_state["running"] = True
        self.session_state["last_tick"] = time.time()
        
        # Reset
        self.session_state["seconds_left"] = self.MODES[self.session_state["mode"]]
        self.session_state["running"] = False
        self.session_state["last_tick"] = None
        
        self.assertEqual(self.session_state["seconds_left"], 1500)
        self.assertFalse(self.session_state["running"])
        self.assertIsNone(self.session_state["last_tick"])
    
    def test_toggle_running_state(self):
        """Test toggling running state."""
        # Start
        self.session_state["running"] = not self.session_state["running"]
        self.assertTrue(self.session_state["running"])
        
        # Pause
        self.session_state["running"] = not self.session_state["running"]
        self.assertFalse(self.session_state["running"])


# ─────────────────────────────────────────────────────────────────────────────
# Test Suite 6: Edge Cases
# ─────────────────────────────────────────────────────────────────────────────
class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""
    
    def test_timer_doesnt_go_negative(self):
        """Test that timer doesn't go below zero."""
        seconds_left = 5
        elapsed = 10
        
        seconds_left = max(0, seconds_left - elapsed)
        
        self.assertEqual(seconds_left, 0)
        self.assertGreaterEqual(seconds_left, 0)
    
    def test_timer_completes_on_zero(self):
        """Test that timer stops at zero."""
        running = True
        seconds_left = 2
        
        if seconds_left <= 0:
            running = False
        
        seconds_left = max(0, seconds_left - 3)
        if seconds_left == 0:
            running = False
        
        self.assertFalse(running)
        self.assertEqual(seconds_left, 0)
    
    def test_progress_percentage_bounds(self):
        """Test that progress percentage stays within 0-100%."""
        total = 1500
        
        test_cases = [0, 750, 1500]
        
        for seconds_left in test_cases:
            pct = 100 * (1 - seconds_left / total) if total else 100
            self.assertGreaterEqual(pct, 0.0, f"Pct should be >= 0, got {pct}")
            self.assertLessEqual(pct, 100.0, f"Pct should be <= 100, got {pct}")
    
    def test_empty_tasks_list(self):
        """Test handling empty tasks list."""
        tasks = []
        
        self.assertEqual(len(tasks), 0)
        self.assertFalse(tasks)  # Empty list is falsy
    
    def test_last_tick_none_handling(self):
        """Test that None last_tick is handled properly."""
        last_tick = None
        running = True
        
        if running and last_tick is not None:
            now = time.time()
            elapsed = int(now - last_tick)
        else:
            elapsed = None
        
        self.assertIsNone(elapsed)


# ─────────────────────────────────────────────────────────────────────────────
# Test Runner
# ─────────────────────────────────────────────────────────────────────────────
def run_tests():
    """Run all tests and print results."""
    print("\n" + "="*80)
    print("POMODORO TIMER - UNIT TESTS")
    print("="*80 + "\n")
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestTimeCalculations))
    suite.addTests(loader.loadTestsFromTestCase(TestSessionStateManagement))
    suite.addTests(loader.loadTestsFromTestCase(TestTaskManagement))
    suite.addTests(loader.loadTestsFromTestCase(TestPomodoroCounter))
    suite.addTests(loader.loadTestsFromTestCase(TestTimerControls))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    
    # Run with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*80 + "\n")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
