"""
Route optimization tools for Agent #3 - Optimize property viewing routes
"""

from typing import List, Dict, Optional, Tuple
from agno.tools import Toolkit
import googlemaps
import os
from datetime import datetime, timedelta
import math


class RouteOptimizationTools(Toolkit):
    def __init__(
        self,
        api_key: str = None,
        default_mode: str = "driving"
    ):
        super().__init__(name="route_optimization_tools")
        
        self.api_key = api_key or os.getenv("GOOGLE_MAPS_API_KEY")
        self.default_mode = default_mode
        
        if self.api_key:
            self.gmaps = googlemaps.Client(key=self.api_key)
        else:
            self.gmaps = None
        
        # Register tools
        self.register(self.calculate_travel_time)
        self.register(self.optimize_viewing_route)
        self.register(self.get_route_directions)
        self.register(self.estimate_total_viewing_time)
        self.register(self.find_optimal_meeting_point)
        self.register(self.check_traffic_conditions)

    def calculate_travel_time(
        self,
        origin: str,
        destination: str,
        departure_time: Optional[str] = None,
        mode: str = None
    ) -> Dict:
        """
        Calculate travel time between two locations
        
        Args:
            origin: Starting location (address or coordinates)
            destination: Destination address
            departure_time: When to depart (ISO format)
            mode: Transportation mode (driving, walking, transit)
            
        Returns:
            Travel time and distance information
        """
        if not self.gmaps:
            return {'error': 'Google Maps API not configured'}
        
        try:
            mode = mode or self.default_mode
            
            # Convert departure time if provided
            departure_datetime = None
            if departure_time:
                departure_datetime = datetime.fromisoformat(departure_time.replace('Z', '+00:00'))
            
            result = self.gmaps.distance_matrix(
                origins=[origin],
                destinations=[destination],
                mode=mode,
                departure_time=departure_datetime,
                traffic_model='best_guess' if mode == 'driving' else None
            )
            
            element = result['rows'][0]['elements'][0]
            
            if element['status'] == 'OK':
                return {
                    'status': 'success',
                    'distance': {
                        'text': element['distance']['text'],
                        'value_meters': element['distance']['value']
                    },
                    'duration': {
                        'text': element['duration']['text'],
                        'value_seconds': element['duration']['value']
                    },
                    'duration_in_traffic': element.get('duration_in_traffic', {
                        'text': element['duration']['text'],
                        'value_seconds': element['duration']['value']
                    }),
                    'origin': origin,
                    'destination': destination,
                    'mode': mode
                }
            else:
                return {
                    'status': 'error',
                    'error': f"Route calculation failed: {element['status']}"
                }
                
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }

    def optimize_viewing_route(
        self,
        properties: List[Dict],
        start_location: str,
        viewing_duration_minutes: int = 90,
        buffer_minutes: int = 15
    ) -> Dict:
        """
        Optimize the route for viewing multiple properties
        
        Args:
            properties: List of properties with addresses
            start_location: Starting point for the route
            viewing_duration_minutes: Time to spend at each property
            buffer_minutes: Buffer time between viewings
            
        Returns:
            Optimized route with timing
        """
        if not self.gmaps or len(properties) <= 1:
            return {
                'status': 'error',
                'error': 'Need Google Maps API and multiple properties'
            }
        
        try:
            # Get all addresses
            addresses = [start_location] + [prop.get('address') for prop in properties]
            
            # Calculate distance matrix between all points
            matrix = self.gmaps.distance_matrix(
                origins=addresses,
                destinations=addresses,
                mode=self.default_mode,
                traffic_model='best_guess'
            )
            
            # Simple greedy optimization (nearest neighbor)
            unvisited = list(range(1, len(addresses)))  # Skip start location
            current_location = 0
            route_order = [0]  # Start with start_location
            total_travel_time = 0
            
            while unvisited:
                nearest_idx = None
                min_duration = float('inf')
                
                for idx in unvisited:
                    duration = matrix['rows'][current_location]['elements'][idx]['duration']['value']
                    if duration < min_duration:
                        min_duration = duration
                        nearest_idx = idx
                
                if nearest_idx is not None:
                    route_order.append(nearest_idx)
                    unvisited.remove(nearest_idx)
                    total_travel_time += min_duration
                    current_location = nearest_idx
                else:
                    break
            
            # Create detailed route with timing
            optimized_route = []
            current_time = datetime.now()
            
            for i, addr_idx in enumerate(route_order):
                if i == 0:  # Start location
                    optimized_route.append({
                        'order': 0,
                        'location': addresses[addr_idx],
                        'type': 'start',
                        'arrival_time': current_time.isoformat(),
                        'departure_time': current_time.isoformat()
                    })
                else:
                    # Calculate travel time from previous location
                    prev_idx = route_order[i-1]
                    travel_duration = matrix['rows'][prev_idx]['elements'][addr_idx]['duration']['value']
                    
                    # Add travel time
                    arrival_time = current_time + timedelta(seconds=travel_duration)
                    departure_time = arrival_time + timedelta(minutes=viewing_duration_minutes)
                    
                    property_data = properties[addr_idx - 1]  # -1 because addresses[0] is start_location
                    
                    optimized_route.append({
                        'order': i,
                        'property_id': property_data.get('id'),
                        'location': addresses[addr_idx],
                        'type': 'viewing',
                        'arrival_time': arrival_time.isoformat(),
                        'departure_time': departure_time.isoformat(),
                        'viewing_duration_minutes': viewing_duration_minutes,
                        'travel_time_from_previous': travel_duration,
                        'property_data': property_data
                    })
                    
                    # Update current time for next iteration
                    current_time = departure_time + timedelta(minutes=buffer_minutes)
            
            # Calculate total time for the entire route
            total_duration = (current_time - datetime.now()).total_seconds() / 60
            
            return {
                'status': 'success',
                'optimized_route': optimized_route,
                'total_properties': len(properties),
                'total_duration_minutes': int(total_duration),
                'total_travel_time_seconds': total_travel_time,
                'estimated_completion_time': current_time.isoformat(),
                'optimization_method': 'nearest_neighbor'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }

    def get_route_directions(
        self,
        origin: str,
        destination: str,
        waypoints: List[str] = None
    ) -> Dict:
        """
        Get detailed driving directions
        
        Args:
            origin: Starting location
            destination: End location
            waypoints: Intermediate stops
            
        Returns:
            Detailed turn-by-turn directions
        """
        if not self.gmaps:
            return {'error': 'Google Maps API not configured'}
        
        try:
            result = self.gmaps.directions(
                origin=origin,
                destination=destination,
                waypoints=waypoints,
                mode=self.default_mode,
                optimize_waypoints=True if waypoints else False
            )
            
            if result:
                route = result[0]
                legs = route['legs']
                
                directions = {
                    'status': 'success',
                    'total_distance': sum(leg['distance']['value'] for leg in legs),
                    'total_duration': sum(leg['duration']['value'] for leg in legs),
                    'overview_polyline': route['overview_polyline']['points'],
                    'legs': []
                }
                
                for i, leg in enumerate(legs):
                    leg_info = {
                        'start_address': leg['start_address'],
                        'end_address': leg['end_address'],
                        'distance': leg['distance'],
                        'duration': leg['duration'],
                        'steps': []
                    }
                    
                    for step in leg['steps']:
                        step_info = {
                            'distance': step['distance'],
                            'duration': step['duration'],
                            'html_instructions': step['html_instructions'],
                            'maneuver': step.get('maneuver', ''),
                            'start_location': step['start_location'],
                            'end_location': step['end_location']
                        }
                        leg_info['steps'].append(step_info)
                    
                    directions['legs'].append(leg_info)
                
                return directions
            else:
                return {'status': 'error', 'error': 'No route found'}
                
        except Exception as e:
            return {'status': 'error', 'error': str(e)}

    def estimate_total_viewing_time(
        self,
        properties: List[Dict],
        start_location: str,
        viewing_duration_minutes: int = 90
    ) -> Dict:
        """
        Estimate total time needed for all viewings including travel
        
        Args:
            properties: List of properties
            start_location: Starting point
            viewing_duration_minutes: Time per property
            
        Returns:
            Time estimation breakdown
        """
        if not properties:
            return {'status': 'error', 'error': 'No properties provided'}
        
        # Get optimized route
        route_result = self.optimize_viewing_route(
            properties, start_location, viewing_duration_minutes
        )
        
        if route_result['status'] != 'success':
            return route_result
        
        route = route_result['optimized_route']
        
        # Calculate breakdown
        total_viewing_time = len(properties) * viewing_duration_minutes
        total_travel_time = route_result['total_travel_time_seconds'] / 60
        buffer_time = (len(properties) - 1) * 15  # 15 min buffer between viewings
        
        return {
            'status': 'success',
            'breakdown': {
                'total_properties': len(properties),
                'viewing_time_minutes': total_viewing_time,
                'travel_time_minutes': int(total_travel_time),
                'buffer_time_minutes': buffer_time,
                'total_time_minutes': int(total_viewing_time + total_travel_time + buffer_time)
            },
            'recommendations': {
                'start_early': 'true' if total_viewing_time + total_travel_time > 240 else 'false',  # 4+ hours
                'split_days': 'true' if len(properties) > 4 else 'false',
                'bring_snacks': 'true' if total_viewing_time + total_travel_time > 180 else 'false'  # 3+ hours
            },
            'schedule': route
        }

    def find_optimal_meeting_point(
        self,
        user_location: str,
        properties: List[Dict]
    ) -> Dict:
        """
        Find optimal meeting point that minimizes total travel
        
        Args:
            user_location: User's starting location
            properties: List of properties to view
            
        Returns:
            Recommended meeting point
        """
        if not self.gmaps or not properties:
            return {'error': 'Google Maps API not configured or no properties'}
        
        try:
            addresses = [user_location] + [prop.get('address') for prop in properties]
            
            # Simple approach: find the geographic center
            geocode_results = []
            for addr in addresses:
                result = self.gmaps.geocode(addr)
                if result:
                    location = result[0]['geometry']['location']
                    geocode_results.append((location['lat'], location['lng']))
            
            if not geocode_results:
                return {'error': 'Could not geocode addresses'}
            
            # Calculate centroid
            center_lat = sum(loc[0] for loc in geocode_results) / len(geocode_results)
            center_lng = sum(loc[1] for loc in geocode_results) / len(geocode_results)
            
            # Find nearest significant location to centroid
            center_point = f"{center_lat},{center_lng}"
            places_result = self.gmaps.places_nearby(
                location=(center_lat, center_lng),
                radius=2000,  # 2km radius
                type='establishment'
            )
            
            meeting_suggestions = []
            if places_result.get('results'):
                for place in places_result['results'][:3]:  # Top 3 suggestions
                    meeting_suggestions.append({
                        'name': place['name'],
                        'address': place.get('vicinity', ''),
                        'place_id': place['place_id'],
                        'rating': place.get('rating', 0),
                        'types': place.get('types', [])
                    })
            
            return {
                'status': 'success',
                'centroid': {
                    'lat': center_lat,
                    'lng': center_lng,
                    'address': center_point
                },
                'meeting_suggestions': meeting_suggestions,
                'total_properties': len(properties)
            }
            
        except Exception as e:
            return {'status': 'error', 'error': str(e)}

    def check_traffic_conditions(
        self,
        origin: str,
        destination: str,
        departure_time: str
    ) -> Dict:
        """
        Check current traffic conditions for a route
        
        Args:
            origin: Start location
            destination: End location  
            departure_time: When to depart (ISO format)
            
        Returns:
            Traffic condition information
        """
        if not self.gmaps:
            return {'error': 'Google Maps API not configured'}
        
        try:
            departure_datetime = datetime.fromisoformat(departure_time.replace('Z', '+00:00'))
            
            # Get route with traffic
            result = self.gmaps.distance_matrix(
                origins=[origin],
                destinations=[destination],
                mode='driving',
                departure_time=departure_datetime,
                traffic_model='best_guess'
            )
            
            element = result['rows'][0]['elements'][0]
            
            if element['status'] == 'OK':
                normal_duration = element['duration']['value']
                traffic_duration = element.get('duration_in_traffic', {}).get('value', normal_duration)
                
                delay_minutes = (traffic_duration - normal_duration) / 60
                
                if delay_minutes > 15:
                    traffic_level = 'heavy'
                    recommendation = 'Consider leaving earlier or choosing a different time'
                elif delay_minutes > 5:
                    traffic_level = 'moderate'
                    recommendation = 'Allow extra time for travel'
                else:
                    traffic_level = 'light'
                    recommendation = 'Good time to travel'
                
                return {
                    'status': 'success',
                    'traffic_level': traffic_level,
                    'normal_duration_minutes': normal_duration / 60,
                    'traffic_duration_minutes': traffic_duration / 60,
                    'delay_minutes': delay_minutes,
                    'recommendation': recommendation,
                    'departure_time': departure_time
                }
            else:
                return {'status': 'error', 'error': f"Traffic check failed: {element['status']}"}
                
        except Exception as e:
            return {'status': 'error', 'error': str(e)}