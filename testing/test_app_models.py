import pytest
from pydantic import ValidationError
from app.models.goal import CreateGoal, ReadGoal
from app.models.todo import CreateTodo, ReadTodo, Priority
from app.models.workout import CreateWorkout, ReadWorkout, WorkoutType

''' GOAL MODEL TESTS '''


# Test 1: Valid CreateGoal
def test_create_goal_valid():
    goal = CreateGoal(title="Learn FastAPI", description="Follow tutorial", deadline="2025-09-01", completed=False)
    assert goal.title == "Learn FastAPI"
    assert goal.completed is False


# Test 2: Missing required 'title'
def test_create_goal_missing_title():
    with pytest.raises(ValidationError):
        CreateGoal(description="Missing title")


# Test 3: Empty description is allowed
def test_create_goal_empty_description():
    goal = CreateGoal(title="Read", description="", deadline="2025-09-01")
    assert goal.description == ""


# Test 4: Deadline is optional
def test_create_goal_no_deadline():
    goal = CreateGoal(title="Stretch", description="Daily habit")
    assert goal.deadline is None


# Test 5: Completed must be a boolean
def test_create_goal_invalid_completed_type():
    with pytest.raises(ValidationError):
        CreateGoal(title="Workout", completed="yes")  # should be boolean


# Test 6: ReadGoal inherits CreateGoal and includes ID
def test_read_goal_valid():
    goal = ReadGoal(id=1, title="Stretch", description="Daily", deadline="2025-08-14", completed=False)
    assert goal.id == 1
    assert isinstance(goal, CreateGoal)



''' TODO MODEL TESTS '''


# Test 7: Valid CreateTodo with priority
def test_create_todo_valid():
    todo = CreateTodo(title="Buy milk", description="Almond milk", priority=Priority.high, completed=False)
    assert todo.priority == Priority.high


# Test 8: Invalid priority (not a valid enum)
def test_create_todo_invalid_priority():
    with pytest.raises(ValidationError):
        CreateTodo(title="Buy milk", priority="urgent")  # invalid enum


# Test 9: ReadTodo inherits CreateTodo and includes ID
def test_read_todo_valid():
    todo = ReadTodo(id=3, title="Laundry", completed=True, priority=Priority.low)
    assert todo.id == 3
    assert todo.priority == Priority.low

# Test 10: Missing required title
def test_create_todo_missing_title():
    with pytest.raises(ValidationError):
        CreateTodo(description="No title")


# Test 11: Empty title string
def test_create_todo_empty_title():
    todo = CreateTodo(title="", description="Empty title test")
    assert todo.title == ""


# Test 12: Priority is optional
def test_create_todo_priority_optional():
    todo = CreateTodo(title="Walk dog")
    assert todo.priority is Priority.medium


# Test 13: Completed defaults to False
def test_create_todo_completed_default():
    todo = CreateTodo(title="Do dishes")
    assert todo.completed is False


# Test 14: Invalid type for completed
def test_create_todo_invalid_completed_type():
    with pytest.raises(ValidationError):
        CreateTodo(title="Clean", completed="done")  # should be bool

''' WORKOUT MODEL TESTS '''

# Test 15: Valid CreateWorkout instance
def test_create_workout_valid():
    workout = CreateWorkout(type=WorkoutType.running, duration_minutes=30)
    assert workout.type == WorkoutType.running
    assert workout.duration_minutes == 30
    assert workout.sets is None
    assert workout.completed is False

# Test 16: Missing required field: type
def test_create_workout_missing_type():
    with pytest.raises(ValidationError):
        CreateWorkout(duration_minutes=45)

# Test 17: Missing required field: duration
def test_create_workout_missing_duration():
    with pytest.raises(ValidationError):
        CreateWorkout(type=WorkoutType.gym)

# Test 18: Invalid workout type
def test_create_workout_invalid_type():
    with pytest.raises(ValidationError):
        CreateWorkout(type="swimming", duration=20)  # Not in enum

# Test 19: Invalid type for duration
def test_create_workout_invalid_duration_type():
    with pytest.raises(ValidationError):
        CreateWorkout(type=WorkoutType.yoga, duration_minutes="forty")  # Should be int

# Test 20: Valid workout with all optional fields
def test_create_workout_with_all_fields():
    workout = CreateWorkout(
        type=WorkoutType.gym,
        duration_minutes=60,
        sets=5,
        notes="Leg day",
        completed=True
    )
    assert workout.sets == 5
    assert workout.notes == "Leg day"
    assert workout.completed is True

# Test 21: ReadWorkout includes ID
def test_read_workout_with_id():
    workout = ReadWorkout(
        id=1,
        type=WorkoutType.running,
        duration_minutes=20
    )
    assert workout.id == 1
    assert workout.type == WorkoutType.running
    assert workout.duration_minutes == 20