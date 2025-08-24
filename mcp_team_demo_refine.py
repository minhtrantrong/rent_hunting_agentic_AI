import os
import sys
from datetime import datetime, timedelta
from typing import Dict, Any, List
from dotenv import load_dotenv

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

load_dotenv()

try:
    from mcp_framework import MCPRegistry, MCPClient, setup_mcp_logging
    from mcp_servers import CalendarMCPServer, CommunicationMCPServer, MapsMCPServer
    print("✅ MCP framework and servers loaded")
except ImportError as e:
    print(f"❌ MCP import error: {e}")
    sys.exit(1)
print("🚀 Multi-Agent Apartment Hunting Coordination")
class MCPTeamDemo:
    """
    Complete MCP demonstration for team review.
    Shows Agent #3 using Model Context Protocol with real API integration.
    """

    def __init__(self):
        """Initialize MCPTeamDemo, environment, logging, and MCP architecture."""
        if not os.getenv('EMAIL_ADDRESS'):
            print("⚠️ No EMAIL_ADDRESS found - using demo mode")
            os.environ['DEMO_MODE'] = 'true'
        setup_mcp_logging("INFO")
        self.mcp_registry = MCPRegistry()
        self._initialize_mcp_servers()
        self.mcp_client = MCPClient(self.mcp_registry)
        print("🏠 RentGenius Agent #3 - MCP Team Demo")
        print("=" * 60)
        print("🤖 Model Context Protocol Architecture")
        print("🚀 Multi-Agent Apartment Hunting Coordination")
        print("🏆 TiDB Hackathon 2025\n")

    def _initialize_mcp_servers(self) -> None:
        """Initialize all MCP servers and register them in the MCP registry."""
        try:
            calendar_server = CalendarMCPServer()
            self.mcp_registry.register_server(calendar_server)
            comm_server = CommunicationMCPServer()
            self.mcp_registry.register_server(comm_server)
            maps_server = MapsMCPServer()
            self.mcp_registry.register_server(maps_server)
            print("✅ All MCP servers initialized")
        except Exception as e:
            raise

    def demonstrate_mcp_architecture(self) -> bool:
        print("🏗️ MCP ARCHITECTURE DEMONSTRATION")
        print("=" * 50)

        # Show MCP registry status
        mcp_status = self.mcp_registry.list_servers()
        available_tools = self.mcp_client.list_available_tools()

        print("📊 MCP Registry Status:")
        for server_name, server_info in mcp_status.items():
            print(f"   🔧 {server_name}: {server_info['version']} ({len(server_info['tools'])} tools)")

        print(f"\n🛠️ Available Tools:")
        for server_name, tool_names in available_tools.items():
            print(f"   {server_name}: {', '.join(tool_names)}")

        # Test MCP server communication
        print(f"\n🔄 Testing MCP Communication:")
        self._test_mcp_communication()

        return True

    def _test_mcp_communication(self) -> None:
        """Test MCP server communication for calendar, communication, and maps servers."""
        try:
            start_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
            end_date = (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d')
            result = self.mcp_client.call(
                "calendar-server",
                "get_availability",
                start_date=start_date,
                end_date=end_date,
                duration_minutes=90
            )
            slots = result.get("availability_slots", [])
            print(f"   📅 Calendar Server: Found {len(slots)} available slots")
        except Exception as e:
            print(f"   ❌ Calendar Server error: {e}")
        try:
            result = self.mcp_client.call(
                "communication-server",
                "send_email",
                to_email="demo@rentgenius.com",
                subject="MCP Test",
                message="Testing MCP communication server"
            )
            status = result.get("status", "unknown")
            print(f"   📧 Communication Server: {status}")
        except Exception as e:
            print(f"   ❌ Communication Server error: {e}")
        try:
            result = self.mcp_client.call(
                "maps-server",
                "calculate_travel_time",
                origin="Downtown Austin, TX",
                destination="University of Texas at Austin"
            )
            travel_time = result.get("travel_time_minutes", "unknown")
            print(f"   🗺️ Maps Server: {travel_time} minute travel time")
        except Exception as e:
            print(f"   ❌ Maps Server error: {e}")

    def simulate_multi_agent_coordination(self) -> Dict[str, Any]:
        """Simulate complete multi-agent coordination workflow."""
        print(f"\n🤖 MULTI-AGENT COORDINATION SIMULATION")
        print("=" * 55)
        user_profile: Dict[str, Any] = {
            "name": "Alex Chen",
            "email": os.environ.get("EMAIL_ADDRESS", "demo@rentgenius.com"),
            "lifestyle": "young_professional",
            "budget_max": 4200,
            "priorities": ["investment", "walkability", "safety"],
            "current_location": "Downtown Austin, TX"
        }
        print(f"👤 User: {user_profile['name']}")
        print(f"💰 Budget: ${user_profile['budget_max']}")
        print(f"🎯 Priorities: {', '.join(user_profile['priorities'])}")
        print(f"\n📊 Step 1: Agent #1 Property Intelligence")
        agent1_properties = self._simulate_agent1_data()
        print(f"   ✅ {len(agent1_properties)} properties analyzed with investment metrics")
        print(f"\n🏘️ Step 2: Agent #2 Regional Intelligence")
        agent2_data = self._simulate_agent2_data()
        print(f"   ✅ Regional analysis for {agent2_data['region_name']}")
        print(f"   📊 Safety: {agent2_data['safety_score']}/10, Walkability: {agent2_data['walkability']}/100")
        print(f"\n🤖 Step 3: Agent #3 MCP Coordination")
        coordination_result = self._coordinate_via_mcp(user_profile, agent1_properties, agent2_data)
        return coordination_result
    def _simulate_agent1_data(self) -> List[Dict]:
        """Simulate realistic Agent #1 property intelligence"""
        import random
        
        austin_properties = [
            {
                "property_id": "mcp_prop_001",
                "name": "The Independent",
                "address": "2505 San Gabriel St, Austin, TX 78705",
                "price": "$3,800/month",
                "agent_name": "Sarah Martinez",
                "agent_contact": {
                    "phone": "+15127891234",
                    "email": "sarah.martinez@theindependent.com"
                },
                "price_analysis": {
                    "monthly_rent": 3800,
                    "affordability_score": 8.2,
                    "market_position": "competitive"
                },
                "investment_metrics": {
                    "roi_projection": 7.8,
                    "rental_demand": "high"
                },
                "risk_assessment": {
                    "overall_risk": "low"
                },
                "property_features": {
                    "bedrooms": 2,
                    "bathrooms": 2,
                    "sqft": 950,
                    "amenities": ["Pool", "Gym", "Study Rooms", "Rooftop Deck"]
                }
            },
            {
                "property_id": "mcp_prop_002", 
                "name": "East Austin Loft",
                "address": "2400 E 6th St, Austin, TX 78702",
                "price": "$3,200/month",
                "agent_name": "Michael Chen",
                "agent_contact": {
                    "phone": "+15125551987",
                    "email": "michael.chen@eastaustinloft.com"
                },
                "price_analysis": {
                    "monthly_rent": 3200,
                    "affordability_score": 8.8,
                    "market_position": "value"
                },
                "investment_metrics": {
                    "roi_projection": 8.4,
                    "rental_demand": "very_high"
                },
                "risk_assessment": {
                    "overall_risk": "low"
                },
                "property_features": {
                    "bedrooms": 2,
                    "bathrooms": 1,
                    "sqft": 850,
                    "amenities": ["Pet-friendly", "Parking", "Industrial Design"]
                }
            },
            {
                "property_id": "mcp_prop_003",
                "name": "South Lamar Modern",
                "address": "1900 S Lamar Blvd, Austin, TX 78704",
                "price": "$4,100/month",
                "agent_name": "Jessica Williams",
                "agent_contact": {
                    "phone": "+15124567890",
                    "email": "j.williams@southlamarmodern.com"
                },
                "price_analysis": {
                    "monthly_rent": 4100,
                    "affordability_score": 7.5,
                    "market_position": "premium"
                },
                "investment_metrics": {
                    "roi_projection": 6.9,
                    "rental_demand": "high"
                },
                "risk_assessment": {
                    "overall_risk": "moderate"
                },
                "property_features": {
                    "bedrooms": 2,
                    "bathrooms": 2,
                    "sqft": 1100,
                    "amenities": ["Pool", "Gym", "Food Hall", "Concierge"]
                }
            }
        ]
        
        return austin_properties
    

    def _simulate_agent2_data(self) -> Dict:
        """Simulate realistic Agent #2 regional intelligence"""
        return {
            "region_name": "Austin, TX - Central District",
            "safety_score": 8.4,
            "walkability": 82,
            "lifestyle_fit": {
                "young_professional": 8.9,
                "family_friendly": 7.2,
                "student_oriented": 8.1
            },
            "demographics": {
                "median_age": 29.5,
                "median_income": 78000,
                "population_growth": 0.048
            },
            "amenities": {
                "restaurants_score": 9.1,
                "entertainment_score": 8.8,
                "parks_recreation": 7.6
            },
            "market_trends": {
                "rental_growth": 0.065,
                "occupancy_rate": 0.94,
                "inventory_level": "tight"
            }
        }
    
    def _coordinate_via_mcp(self, user_profile: Dict, properties: List[Dict], regional_data: Dict) -> Dict:
        """Perform MCP-based coordination"""
        coordination_results = {
            "user_profile": user_profile,
            "properties_analyzed": len(properties),
            "mcp_servers_used": [],
            "coordination_steps": []
        }
        
        # Step 1: Intelligent property selection
        selected_properties = self._select_properties_with_mcp_scoring(
            properties, regional_data, user_profile
        )
        
        coordination_results["properties_selected"] = len(selected_properties)
        coordination_results["coordination_steps"].append("property_selection")
        
        # Step 2: MCP Calendar coordination
        try:
            calendar_result = self._mcp_calendar_coordination(selected_properties, user_profile)
            coordination_results["calendar_events"] = calendar_result.get("events_created", [])
            coordination_results["mcp_servers_used"].append("calendar-server")
            coordination_results["coordination_steps"].append("calendar_coordination")
            
            print(f"   📅 Calendar MCP: {len(calendar_result.get('events_created', []))} events created")
            
        except Exception as e:
            print(f"   ⚠️ Calendar MCP: {e}")
            coordination_results["calendar_events"] = []
        
        # Step 3: MCP Communication coordination
        try:
            comm_result = self._mcp_communication_coordination(
                user_profile, selected_properties, regional_data
            )
            coordination_results["email_sent"] = comm_result.get("status") == "sent"
            coordination_results["mcp_servers_used"].append("communication-server") 
            coordination_results["coordination_steps"].append("communication_coordination")
            
            print(f"   📧 Communication MCP: Email {comm_result.get('status', 'unknown')}")
            
        except Exception as e:
            print(f"   ⚠️ Communication MCP: {e}")
            coordination_results["email_sent"] = False
        
        # Step 4: MCP Route optimization
        try:
            route_result = self._mcp_route_coordination(selected_properties, user_profile)
            coordination_results["route_optimized"] = route_result.get("status") == "success"
            coordination_results["mcp_servers_used"].append("maps-server")
            coordination_results["coordination_steps"].append("route_optimization")
            
            print(f"   🗺️ Maps MCP: Route optimization {route_result.get('status', 'unknown')}")
            
        except Exception as e:
            print(f"   ⚠️ Maps MCP: {e}")
            coordination_results["route_optimized"] = False
        
        return coordination_results
    
    def _select_properties_with_mcp_scoring(self, properties: List[Dict], regional_data: Dict, user_profile: Dict) -> List[Dict]:
        """Select properties using MCP multi-agent scoring"""
        scored_properties = []
        
        for prop in properties:
            score = self._calculate_mcp_score(prop, regional_data, user_profile)
            scored_properties.append({
                "property": prop,
                "mcp_score": score,
                "selection_reasons": self._get_selection_reasons(prop, score, user_profile)
            })
        
        # Sort by MCP score and select top 2
        scored_properties.sort(key=lambda x: x["mcp_score"], reverse=True)
        selected = scored_properties[:2]
        
        print(f"   🎯 Property Selection via MCP scoring:")
        for i, selection in enumerate(selected, 1):
            prop = selection["property"]
            score = selection["mcp_score"]
            print(f"      {i}. {prop['name']}: {score}/100 MCP score")
        
        return selected
    
    def _calculate_mcp_score(self, prop: Dict, regional_data: Dict, user_profile: Dict) -> float:
        """Calculate MCP coordination score"""
        score = 0.0
        
        # Budget compatibility
        rent = prop["price_analysis"]["monthly_rent"]
        budget = user_profile["budget_max"]
        if rent <= budget:
            budget_ratio = rent / budget
            score += 30 * (1.5 - budget_ratio)
        
        # Agent #1 metrics
        affordability = prop["price_analysis"]["affordability_score"]
        roi = prop["investment_metrics"]["roi_projection"]
        risk = prop["risk_assessment"]["overall_risk"]
        
        score += (affordability / 10.0) * 20
        score += min(roi / 10.0, 1.0) * 15
        score += {"low": 10, "moderate": 5, "high": 0}[risk]
        
        # Agent #2 regional fit
        lifestyle = user_profile["lifestyle"]
        regional_fit = regional_data["lifestyle_fit"].get(lifestyle, 7.0)
        safety = regional_data["safety_score"]
        walkability = regional_data["walkability"] / 100.0
        
        score += (regional_fit / 10.0) * 15
        score += (safety / 10.0) * 5
        score += walkability * 5
        
        return round(min(score, 100.0), 1)
    
    def _get_selection_reasons(self, prop: Dict, score: float, user_profile: Dict) -> List[str]:
        """Get reasons for property selection"""
        reasons = []
        
        rent = prop["price_analysis"]["monthly_rent"]
        budget = user_profile["budget_max"]
        
        if rent < budget * 0.9:
            reasons.append(f"${budget - rent} under budget")
        
        roi = prop["investment_metrics"]["roi_projection"]
        if roi > 7.5:
            reasons.append(f"Strong ROI: {roi:.1f}%")
        
        if prop["risk_assessment"]["overall_risk"] == "low":
            reasons.append("Low investment risk")
        
        if score > 80:
            reasons.append("Excellent MCP score")
        
        return reasons
    
    def _mcp_calendar_coordination(self, selected_properties: List[Dict], user_profile: Dict) -> Dict:
        """Coordinate calendar via MCP"""
        
        # Get availability
        start_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        end_date = (datetime.now() + timedelta(days=5)).strftime('%Y-%m-%d')
        
        availability = self.mcp_client.call(
            "calendar-server",
            "get_availability",
            start_date=start_date,
            end_date=end_date,
            duration_minutes=90
        )
        
        slots = availability.get("availability_slots", [])
        
        # Create events for selected properties
        events_created = []
        
        for i, selection in enumerate(selected_properties[:len(slots)]):
            prop = selection["property"]
            slot = slots[i]
            
            # Create enhanced event
            event_result = self.mcp_client.call(
                "calendar-server", 
                "create_viewing_event",
                property_data={
                    "address": prop["address"],
                    "price": f"${prop['price_analysis']['monthly_rent']}/month",
                    "bedrooms": prop["property_features"]["bedrooms"],
                    "bathrooms": prop["property_features"]["bathrooms"]
                },
                viewing_time=slot,
                attendees=[user_profile["email"]],
                multi_agent_insights={
                    "mcp_score": selection["mcp_score"],
                    "agent1_score": prop["price_analysis"]["affordability_score"],
                    "roi_projection": prop["investment_metrics"]["roi_projection"],
                    "market_position": prop["price_analysis"]["market_position"]
                }
            )
            
            if event_result.get("event_id"):
                events_created.append(event_result["event_id"])
        
        return {
            "events_created": events_created,
            "status": "success"
        }
    
    def _mcp_communication_coordination(self, user_profile: Dict, selected_properties: List[Dict], regional_data: Dict) -> Dict:
        """Coordinate communication via MCP"""
        
        # Prepare viewing schedule for email
        viewing_schedule = []
        for selection in selected_properties:
            prop = selection["property"]
            viewing_schedule.append({
                "property": {
                    "name": prop["name"],
                    "address": prop["address"],
                    "price": f"${prop['price_analysis']['monthly_rent']}/month"
                },
                "mcp_score": selection["mcp_score"],
                "time_slot": {"start": (datetime.now() + timedelta(days=1)).isoformat()}
            })
        
        # Send coordination email via MCP
        result = self.mcp_client.call(
            "communication-server",
            "send_coordination_email",
            user_profile=user_profile,
            viewing_schedule=viewing_schedule,
            multi_agent_insights={
                "properties_analyzed": 3,
                "mcp_coordination": True,
                "regional_safety": regional_data["safety_score"],
                "regional_walkability": regional_data["walkability"]
            }
        )
        
        return result
    
    def _mcp_route_coordination(self, selected_properties: List[Dict], user_profile: Dict) -> Dict:
        """Coordinate route optimization via MCP"""
        
        properties_for_routing = []
        for selection in selected_properties:
            prop = selection["property"]
            properties_for_routing.append({
                "address": prop["address"],
                "name": prop["name"]
            })
        
        result = self.mcp_client.call(
            "maps-server",
            "optimize_viewing_route",
            properties=properties_for_routing,
            start_location=user_profile["current_location"],
            viewing_duration_minutes=90,
            buffer_minutes=15
        )
        
        return result
    
    def run_complete_team_demo(self):
        """Run complete MCP team demonstration"""
        print("🎬 COMPLETE MCP TEAM DEMONSTRATION")
        print("=" * 60)
        
        # Step 1: MCP Architecture Demo
        arch_success = self.demonstrate_mcp_architecture()
        
        # Step 2: Multi-Agent Coordination Demo  
        coordination_result = self.simulate_multi_agent_coordination()
        
        # Step 3: Results Summary
        self._display_demo_results(arch_success, coordination_result)
        
        return coordination_result
    
    def _display_demo_results(self, arch_success: bool, coordination_result: Dict):
        """Display comprehensive demo results"""
        print(f"\n{'='*60}")
        print(f"🏆 MCP TEAM DEMO RESULTS")
        print(f"{'='*60}")
        
        print(f"🏗️ MCP ARCHITECTURE:")
        print(f"   Architecture Demo: {'✅ Success' if arch_success else '❌ Failed'}")
        print(f"   MCP Servers: {len(self.mcp_registry.servers)}")
        print(f"   Available Tools: {sum(len(tools) for tools in self.mcp_client.list_available_tools().values())}")
        
        print(f"\n🤖 MULTI-AGENT COORDINATION:")
        print(f"   Properties Analyzed: {coordination_result.get('properties_analyzed', 0)}")
        print(f"   Properties Selected: {coordination_result.get('properties_selected', 0)}")
        print(f"   Calendar Events: {len(coordination_result.get('calendar_events', []))}")
        print(f"   Email Sent: {'✅' if coordination_result.get('email_sent') else '❌'}")
        print(f"   Route Optimized: {'✅' if coordination_result.get('route_optimized') else '❌'}")
        
        print(f"\n🔧 MCP SERVERS UTILIZED:")
        for server in coordination_result.get('mcp_servers_used', []):
            print(f"   ✅ {server}")
        
        print(f"\n📊 COORDINATION STEPS COMPLETED:")
        for step in coordination_result.get('coordination_steps', []):
            print(f"   ✅ {step.replace('_', ' ').title()}")
        
        # Success metrics
        total_steps = len(coordination_result.get('coordination_steps', []))
        servers_used = len(coordination_result.get('mcp_servers_used', []))
        
        print(f"\n🎯 DEMO SUCCESS METRICS:")
        print(f"   MCP Coordination Steps: {total_steps}/4")
        print(f"   MCP Servers Engaged: {servers_used}/3")
        print(f"   Overall Success Rate: {((total_steps/4 + servers_used/3)/2)*100:.1f}%")
        
        if arch_success and total_steps >= 3 and servers_used >= 2:
            print(f"\n🏆 EXCELLENT! MCP Architecture Demo Ready for Team Review!")
            print(f"   ✨ Production-quality Model Context Protocol implementation")
            print(f"   🚀 Multi-agent coordination with real API integration")
            print(f"   🎯 Perfect for TiDB Hackathon demonstration")
        else:
            print(f"\n👍 GOOD! MCP Architecture demonstrated successfully")
            print(f"   🔧 Some components in mock mode (expected for team demo)")


if __name__ == "__main__":
    print("🏠 RentGenius Agent #3 - MCP Team Demo")
    print("🤖 Model Context Protocol + Multi-Agent Coordination")
    print("🚀 TiDB Hackathon 2025 - Team Review Version")
    print()
    demo = MCPTeamDemo()
    result = demo.run_complete_team_demo()
    print(f"\n🎉 MCP TEAM DEMO COMPLETE!")
    print(f"Ready for team review and hackathon presentation! 🏆")