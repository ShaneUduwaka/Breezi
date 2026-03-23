"""
MockDataLoader - Template-based test data configuration
Loads all test scenarios from testdata.JSON instead of hardcoding
This ensures the system remains configuration-driven, not code-driven
"""

import json
import os


class MockDataLoader:
    """Load test scenarios from configuration file"""

    def __init__(self, testdata_path=None):
        """
        Initialize MockDataLoader
        
        Args:
            testdata_path: Path to testdata.JSON. If None, looks in Business input/
        """
        if testdata_path is None:
            # Find the testdata.JSON relative to this file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            testdata_path = os.path.join(
                current_dir, "..", "Business input", "testdata.JSON"
            )
        
        testdata_path = os.path.abspath(testdata_path)
        
        if not os.path.exists(testdata_path):
            raise FileNotFoundError(
                f"testdata.JSON not found at {testdata_path}\n"
                "Please ensure Business input/testdata.JSON exists"
            )
        
        with open(testdata_path, "r", encoding="utf-8") as f:
            self.test_data = json.load(f)
        
        self.scenarios = self.test_data.get("test_scenarios", {})

    def get_scenario(self, scenario_name):
        """
        Get a test scenario by name
        
        Args:
            scenario_name: Name of scenario (e.g., "pizza_order_incomplete")
            
        Returns:
            dict: Scenario configuration
            
        Raises:
            KeyError: If scenario not found
        """
        if scenario_name not in self.scenarios:
            available = list(self.scenarios.keys())
            raise KeyError(
                f"Scenario '{scenario_name}' not found.\n"
                f"Available scenarios: {available}"
            )
        
        return self.scenarios[scenario_name]

    def get_all_scenarios(self):
        """Get all available scenarios"""
        return self.scenarios

    def scenario_names(self):
        """Get list of all scenario names"""
        return list(self.scenarios.keys())

    def get_input(self, scenario_name):
        """Get user input for a scenario"""
        scenario = self.get_scenario(scenario_name)
        return scenario.get("input")

    def get_slot_updates(self, scenario_name):
        """
        Get slot updates to simulate for a scenario
        
        Returns:
            dict: Mapping of {slot_name: value}
        """
        scenario = self.get_scenario(scenario_name)
        return scenario.get("slot_updates", {})

    def get_expected_intent(self, scenario_name):
        """Get expected intent for a scenario"""
        scenario = self.get_scenario(scenario_name)
        return scenario.get("expected_intent")

    def get_expected_entities(self, scenario_name):
        """Get expected entities for a scenario"""
        scenario = self.get_scenario(scenario_name)
        return scenario.get("expected_entities", {})

    def get_expected_in_response(self, scenario_name):
        """Get words expected in response for a scenario"""
        scenario = self.get_scenario(scenario_name)
        return scenario.get("expected_in_response", [])

    def get_description(self, scenario_name):
        """Get scenario description"""
        scenario = self.get_scenario(scenario_name)
        return scenario.get("description", "")

    def get_default_scenario(self):
        """Get the default scenario (for when none specified)"""
        default = self.test_data.get("default_scenario")
        if default and default in self.scenarios:
            return default
        # Fallback to first scenario
        first_name = list(self.scenarios.keys())[0] if self.scenarios else None
        return first_name

    def print_scenarios(self):
        """Print all available scenarios (useful for CLI help)"""
        print("\n" + "="*70)
        print("📋 AVAILABLE TEST SCENARIOS")
        print("="*70)
        for name, scenario in self.scenarios.items():
            print(f"\n{name}")
            print(f"  └─ {scenario.get('description')}")
            print(f"     Input: '{scenario.get('input')}'")
            print(f"     Intent: {scenario.get('expected_intent')}")


# Example usage:
if __name__ == "__main__":
    loader = MockDataLoader()
    
    print("✅ Test scenarios loaded successfully!")
    loader.print_scenarios()
    
    print("\n" + "="*70)
    print("EXAMPLE: Getting scenario data")
    print("="*70)
    
    scenario_name = "pizza_order_incomplete"
    print(f"\nScenario: {scenario_name}")
    print(f"Input: {loader.get_input(scenario_name)}")
    print(f"Slot updates: {loader.get_slot_updates(scenario_name)}")
    print(f"Expected intent: {loader.get_expected_intent(scenario_name)}")
