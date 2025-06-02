# stub-out python file
import eel

@eel.expose
def solveTriangle(sideA, sideB, angleC):
    """Stub: Solve a right triangle (to be implemented)."""
    return {"error": "Triangle solver not implemented yet"}

@eel.expose
def calculateGeometry(calcType, params):
    """Stub: Calculate geometry (bolt circle or arc length, to be implemented)."""
    return {"error": f"Geometry calculation ({calcType}) not implemented yet"}

@eel.expose
def evaluateMacro(macro):
    """Stub: Evaluate a Fanuc-style macro (to be implemented)."""
    return {"error": "Macro evaluator not implemented yet"}

@eel.expose
def testPyConnection():
    """Stub: Test Python backend connection (to be implemented)."""
    return "Calculator backend not implemented yet"