"""
RentGenius Agent #3 - MCP-Powered Personal Assistant
Multi-agent apartment hunting coordination using Model Context Protocol
"""

import os
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass

from mcp_framework import MCPRegistry, MCPClient, setup_mcp_logging
from mcp_servers import CalendarMCPServer, CommunicationMCPServer, MapsMCPServer
from tidb_shared_memory import TiDBSharedMemory

@dataclass
class CoordinationRequest:
    """Request for apartment viewing coordination"""
    user_profile: Dict[str, Any]
    location: str
    property_limit: int
    preferences: Dict[str, Any]
    request_id: str

@dataclass 
class CoordinationResult:
    """Result of apartment viewing coordination"""
    request_id: str
    status: str
    properties_analyzed: int
    viewings_scheduled: int
    calendar_events_created: List[str]
    email_sent: bool
    multi_agent_insights: Dict[str, Any]
    mcp_servers_used: List[str]
    processing_time_seconds: float

class MCPAgent3:
    """
    RentGenius Agent #3 - MCP-Powered Personal Assistant
    Uses Model Context Protocol for standardized API integrations
    """
    
    def __init__(self, tidb_connection: Optional[str] = None):
        # Setup logging
        setup_mcp_logging("INFO")
        self.logger = logging.getLogger("Agent3.MCP")
        
        # Initialize MCP Registry and Servers
        self.mcp_registry = MCPRegistry()
        self._initialize_mcp_servers()
        
        # Create MCP client for easy tool calling
        self.mcp_client = MCPClient(self.mcp_registry)
        
        # Initialize TiDB shared memory for multi-agent coordination
        self.shared_memory = TiDBSharedMemory(tidb_connection)
        
        # State tracking
        self.active_requests: Dict[str, CoordinationRequest] = {}
        self.coordination_history: List[CoordinationResult] = []
        
        self.logger.info("🏠 Agent #3 MCP initialized with servers: %s", 
                        list(self.mcp_registry.servers.keys()))
    
    def _initialize_mcp_servers(self):
        """Initialize and register all MCP servers"""
        try:
            # Calendar MCP Server
            calendar_server = CalendarMCPServer()
            self.mcp_registry.register_server(calendar_server)
            
            # Communication MCP Server
            comm_server = CommunicationMCPServer()
            self.mcp_registry.register_server(comm_server)
            
            # Maps MCP Server  
            maps_server = MapsMCPServer()
            self.mcp_registry.register_server(maps_server)
            
            self.logger.info("✅ All MCP servers initialized successfully")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize MCP servers: {e}")
            raise
    
    def get_mcp_status(self) -> Dict[str, Any]:
        """Get status of all MCP servers"""
        return {
            "servers": self.mcp_registry.list_servers(),
            "available_tools": self.mcp_client.list_available_tools(),
            "total_servers": len(self.mcp_registry.servers),
            "status": "operational"
        }
    
    def coordinate_apartment_viewings(self, request: CoordinationRequest) -> CoordinationResult:
        """
        Main coordination method using MCP architecture
        
        Args:
            request: Coordination request with user profile and preferences
            
        Returns:
            CoordinationResult with all coordination details
        """
        start_time = datetime.now()
        self.active_requests[request.request_id] = request
        
        self.logger.info(f"🤖 Starting MCP coordination for request {request.request_id}")
        
        try:
            # Step 1: Get multi-agent data
            multi_agent_data = self._gather_multi_agent_intelligence(request)
            
            # Step 2: Intelligent property selection
            selected_properties = self._select_optimal_properties(
                multi_agent_data["properties"],
                multi_agent_data["regional_data"], 
                request.user_profile,
                request.preferences
            )
            
            # Step 3: MCP Calendar Coordination
            calendar_result = self._coordinate_calendar_via_mcp(
                selected_properties,
                request.preferences
            )
            
            # Step 4: MCP Route Optimization
            route_result = self._optimize_route_via_mcp(
                selected_properties,
                request.user_profile.get("current_location", request.location)
            )
            
            # Step 5: MCP Communication Coordination
            communication_result = self._coordinate_communication_via_mcp(
                request.user_profile,
                selected_properties,
                calendar_result,
                multi_agent_data
            )
            
            # Step 6: Generate coordination result
            coordination_result = CoordinationResult(
                request_id=request.request_id,
                status="completed",
                properties_analyzed=len(multi_agent_data["properties"]),
                viewings_scheduled=len(selected_properties),
                calendar_events_created=calendar_result.get("event_ids", []),
                email_sent=communication_result.get("status") == "sent",
                multi_agent_insights=multi_agent_data,
                mcp_servers_used=["calendar-server", "communication-server", "maps-server"],
                processing_time_seconds=(datetime.now() - start_time).total_seconds()
            )
            
            # Store result
            self.coordination_history.append(coordination_result)
            
            self.logger.info(f"✅ MCP coordination completed for {request.request_id}")
            
            return coordination_result
            
        except Exception as e:
            self.logger.error(f"❌ MCP coordination failed: {e}")
            
            # Return error result
            return CoordinationResult(
                request_id=request.request_id,
                status="error",
                properties_analyzed=0,
                viewings_scheduled=0,
                calendar_events_created=[],
                email_sent=False,
                multi_agent_insights={"error": str(e)},
                mcp_servers_used=[],
                processing_time_seconds=(datetime.now() - start_time).total_seconds()
            )
    
    def _gather_multi_agent_intelligence(self, request: CoordinationRequest) -> Dict[str, Any]:
        """Gather data from Agent #1 and Agent #2"""
        self.logger.info("📊 Gathering multi-agent intelligence...")
        
        # Get property data from Agent #1 (via TiDB shared memory)
        properties = self.shared_memory.get_properties_from_agent1(
            request.location, 
            request.property_limit
        )
        
        # Get regional data from Agent #2 (via TiDB shared memory)
        regional_data = self.shared_memory.get_regional_stats_from_agent2(
            request.location
        )
        
        # Log data retrieval
        self.shared_memory.store_agent_data(
            agent_id="agent_3",
            data_type="mcp_coordination_start",
            data={
                "request_id": request.request_id,
                "properties_retrieved": len(properties),
                "regional_data_available": bool(regional_data),
                "mcp_architecture": True,
                "timestamp": datetime.now().isoformat()
            }
        )
        
        return {
            "properties": properties,
            "regional_data": regional_data,
            "retrieval_timestamp": datetime.now().isoformat()
        }
    
    def _select_optimal_properties(self, properties: List[Dict], regional_data: Dict, user_profile: Dict, preferences: Dict) -> List[Dict]:
        """Select optimal properties using multi-agent intelligence"""
        self.logger.info("🎯 Selecting optimal properties with multi-agent scoring...")
        
        scored_properties = []
        
        for prop in properties:
            score = self._calculate_mcp_coordination_score(
                prop, user_profile, regional_data, preferences
            )
            
            scored_properties.append({
                "property": prop,
                "coordination_score": score,
                "selected_reasons": self._generate_selection_reasons(prop, score, user_profile)
            })
        
        # Sort by coordination score and select top properties
        scored_properties.sort(key=lambda x: x["coordination_score"], reverse=True)
        
        # Select based on urgency and preferences
        urgency = preferences.get("urgency", "moderate")
        max_properties = {"high": 4, "moderate": 3, "low": 2}[urgency]
        
        selected = scored_properties[:max_properties]
        
        self.logger.info(f"✅ Selected {len(selected)} properties for coordination")
        
        return selected
    
    def _coordinate_calendar_via_mcp(self, selected_properties: List[Dict], preferences: Dict) -> Dict[str, Any]:
        """Coordinate calendar scheduling via MCP Calendar Server"""
        self.logger.info("📅 Coordinating calendar via MCP Calendar Server...")
        
        try:
            # Get availability via MCP
            start_date = preferences.get("start_date", (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"))
            end_date = preferences.get("end_date", (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"))
            
            availability_result = self.mcp_client.call(
                "calendar-server",
                "get_availability",
                start_date=start_date,
                end_date=end_date,
                duration_minutes=preferences.get("duration_minutes", 90)
            )
            
            available_slots = availability_result["availability_slots"]
            
            # Create viewing schedule
            viewing_schedule = []
            event_ids = []
            
            for i, selected_prop in enumerate(selected_properties[:len(available_slots)]):
                slot = available_slots[i]
                
                # Prepare viewing data for MCP
                viewing_data = {
                    "property": selected_prop["property"],
                    "time_slot": slot,
                    "coordination_score": selected_prop["coordination_score"],
                    "insights": {
                        "agent1_score": selected_prop["property"].get("price_analysis", {}).get("affordability_score", 7.0),
                        "market_position": selected_prop["property"].get("price_analysis", {}).get("market_position", "competitive"),
                        "roi_projection": selected_prop["property"].get("investment_metrics", {}).get("roi_projection", 6.0),
                        "coordination_score": selected_prop["coordination_score"]
                    }
                }
                
                viewing_schedule.append(viewing_data)
            
            # Create bulk events via MCP
            if viewing_schedule:
                user_email = os.environ.get("EMAIL_ADDRESS")
                
                bulk_result = self.mcp_client.call(
                    "calendar-server",
                    "create_bulk_viewing_events",
                    viewing_schedule=viewing_schedule,
                    user_email=user_email
                )
                
                # Extract event IDs
                for result in bulk_result.get("results", []):
                    event_result = result.get("result", {})
                    if event_result.get("event_id"):
                        event_ids.append(event_result["event_id"])
            
            return {
                "status": "success",
                "viewing_schedule": viewing_schedule,
                "event_ids": event_ids,
                "total_events": len(event_ids),
                "mcp_server": "calendar-server"
            }
            
        except Exception as e:
            self.logger.error(f"❌ Calendar coordination failed: {e}")
            return {
                "status": "error",
                "error": str(e),
                "viewing_schedule": [],
                "event_ids": []
            }
    
    def _optimize_route_via_mcp(self, selected_properties: List[Dict], start_location: str) -> Dict[str, Any]:
        """Optimize viewing route via MCP Maps Server"""
        self.logger.info("🗺️ Optimizing route via MCP Maps Server...")
        
        try:
            # Extract property data for route optimization
            properties_for_routing = [
                {
                    "address": prop["property"].get("address"),
                    "name": prop["property"].get("name", "Property")
                }
                for prop in selected_properties
            ]
            
            route_result = self.mcp_client.call(
                "maps-server",
                "optimize_viewing_route",
                properties=properties_for_routing,
                start_location=start_location,
                viewing_duration_minutes=90,
                buffer_minutes=15
            )
            
            return {
                "status": "success",
                "route_optimization": route_result,
                "mcp_server": "maps-server"
            }
            
        except Exception as e:
            self.logger.error(f"❌ Route optimization failed: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    def _coordinate_communication_via_mcp(self, user_profile: Dict, selected_properties: List[Dict], calendar_result: Dict, multi_agent_data: Dict) -> Dict[str, Any]:
        """Coordinate email communication via MCP Communication Server"""
        self.logger.info("📧 Coordinating communication via MCP Communication Server...")
        
        try:
            # Prepare viewing schedule for email
            viewing_schedule = calendar_result.get("viewing_schedule", [])
            
            # Add multi-agent insights to email
            insights = {
                "total_properties_analyzed": len(multi_agent_data.get("properties", [])),
                "regional_data_integrated": bool(multi_agent_data.get("regional_data")),
                "mcp_coordination": True,
                "coordination_timestamp": datetime.now().isoformat()
            }
            
            # Send coordination email via MCP
            comm_result = self.mcp_client.call(
                "communication-server",
                "send_coordination_email",
                user_profile=user_profile,
                viewing_schedule=viewing_schedule,
                multi_agent_insights=insights,
                template_style="professional"
            )
            
            return {
                "status": comm_result.get("status", "sent"),
                "mcp_server": "communication-server",
                "email_details": comm_result
            }
            
        except Exception as e:
            self.logger.error(f"❌ Communication coordination failed: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    def _calculate_mcp_coordination_score(self, property_data: Dict, user_profile: Dict, regional_data: Dict, preferences: Dict) -> float:
        """Calculate coordination score using MCP multi-agent intelligence"""
        score = 0.0
        
        # Budget compatibility (30 points)
        price_analysis = property_data.get("price_analysis", {})
        monthly_rent = price_analysis.get("monthly_rent", 3000)
        user_budget = user_profile.get("budget_max", 3000)
        
        if monthly_rent <= user_budget:
            budget_efficiency = (user_budget - monthly_rent) / user_budget
            score += 30 * (0.7 + budget_efficiency * 0.3)
        
        # Agent #1 intelligence (25 points)
        affordability = price_analysis.get("affordability_score", 7.0)
        investment_metrics = property_data.get("investment_metrics", {})
        roi_projection = investment_metrics.get("roi_projection", 6.0)
        risk_assessment = property_data.get("risk_assessment", {})
        risk_level = risk_assessment.get("overall_risk", "moderate")
        
        score += (affordability / 10.0) * 15  # Max 15 points
        score += min(roi_projection / 10.0, 1.0) * 10  # Max 10 points
        risk_bonus = {"low": 5, "moderate": 0, "high": -5}.get(risk_level, 0)
        score += risk_bonus
        
        # Agent #2 regional intelligence (25 points)
        if regional_data:
            lifestyle_fit = regional_data.get("lifestyle_fit", {})
            user_lifestyle = user_profile.get("lifestyle", "young_professional")
            regional_compatibility = lifestyle_fit.get(user_lifestyle, 7.0)
            
            safety_metrics = regional_data.get("safety_metrics", {})
            safety_score = safety_metrics.get("safety_score", 7.0)
            
            transport_scores = regional_data.get("transport_scores", {})
            walkability = transport_scores.get("walkability", 70) / 100.0
            
            score += (regional_compatibility / 10.0) * 15  # Max 15 points
            score += (safety_score / 10.0) * 5  # Max 5 points
            score += walkability * 5  # Max 5 points
        else:
            score += 12.5  # Default regional score when data unavailable
        
        # User preference alignment (20 points)
        user_priorities = user_profile.get("priorities", [])
        preference_score = 0
        
        for priority in user_priorities:
            if priority == "luxury" and monthly_rent > 4000:
                preference_score += 5
            elif priority == "value" and affordability > 8.0:
                preference_score += 5
            elif priority == "investment" and roi_projection > 8.0:
                preference_score += 5
            elif priority == "safety" and regional_data and regional_data.get("safety_metrics", {}).get("safety_score", 0) > 8.5:
                preference_score += 5
        
        score += min(preference_score, 20)
        
        return round(min(score, 100.0), 1)
    
    def _generate_selection_reasons(self, property_data: Dict, score: float, user_profile: Dict) -> List[str]:
        """Generate reasons why this property was selected"""
        reasons = []
        
        # Budget reasons
        monthly_rent = property_data.get("price_analysis", {}).get("monthly_rent", 3000)
        user_budget = user_profile.get("budget_max", 3000)
        if monthly_rent < user_budget * 0.9:
            reasons.append(f"Excellent value - ${user_budget - monthly_rent} under budget")
        
        # Investment reasons
        roi = property_data.get("investment_metrics", {}).get("roi_projection", 0)
        if roi > 7.0:
            reasons.append(f"Strong investment potential ({roi:.1f}% ROI)")
        
        # Risk reasons
        risk = property_data.get("risk_assessment", {}).get("overall_risk", "moderate")
        if risk == "low":
            reasons.append("Low risk investment")
        
        # Score-based reason
        if score > 80:
            reasons.append("High MCP coordination score")
        elif score > 65:
            reasons.append("Good MCP coordination score")
        
        return reasons or ["Selected by MCP multi-agent coordination"]
    
    def get_coordination_history(self) -> List[CoordinationResult]:
        """Get history of coordination requests"""
        return self.coordination_history
    
    def get_active_requests(self) -> Dict[str, CoordinationRequest]:
        """Get currently active coordination requests"""
        return self.active_requests

# Factory function for easy initialization
def create_mcp_agent3(
    tidb_connection: Optional[str] = None,
    log_level: str = "INFO"
) -> MCPAgent3:
    """
    Create and initialize MCP-powered Agent #3
    
    Args:
        tidb_connection: Optional TiDB connection string
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
    
    Returns:
        Fully initialized MCPAgent3 instance
    """
    setup_mcp_logging(log_level)
    
    return MCPAgent3(tidb_connection)

if __name__ == "__main__":
    # Test MCP Agent #3
    print("🏠 Testing RentGenius MCP Agent #3...")
    
    agent = create_mcp_agent3()
    status = agent.get_mcp_status()
    
    print(f"✅ MCP Agent #3 initialized")
    print(f"📊 MCP Servers: {status['total_servers']}")
    print(f"🔧 Available Tools: {sum(len(tools) for tools in status['available_tools'].values())}")
    print("\n🏆 MCP Agent #3 ready for apartment hunting coordination!")