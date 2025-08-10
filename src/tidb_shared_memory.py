"""
TiDB Shared Memory Integration for RentGenius Multi-Agent System
Enables Agent #3 to receive data from Agent #1 (Properties) and Agent #2 (Regional Stats)
"""

import os
import json
import pymysql
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import logging

class TiDBSharedMemory:
    """TiDB-based shared memory for multi-agent coordination"""
    
    def __init__(self, connection_string: Optional[str] = None):
        self.connection_string = connection_string or os.environ.get('TIDB_CONNECTION_STRING')
        self.connection = None
        self.logger = logging.getLogger(__name__)
        
        if not self.connection_string:
            self.logger.warning("No TiDB connection string provided. Using mock mode.")
            self.mock_mode = True
        else:
            self.mock_mode = False
            self._connect()
    
    def _connect(self):
        """Connect to TiDB Serverless"""
        try:
            # Parse connection string format: mysql://user:password@host:port/database?ssl=true
            import urllib.parse
            parsed = urllib.parse.urlparse(self.connection_string)
            
            self.connection = pymysql.connect(
                host=parsed.hostname,
                port=parsed.port or 4000,
                user=parsed.username,
                password=parsed.password,
                database=parsed.path.lstrip('/'),
                ssl={'ca': None},  # TiDB Serverless uses SSL
                autocommit=True
            )
            
            self.logger.info("✅ Connected to TiDB Serverless")
            self._create_tables()
            
        except Exception as e:
            self.logger.error(f"❌ TiDB connection failed: {e}")
            self.mock_mode = True
    
    def _create_tables(self):
        """Create tables for agent communication"""
        if self.mock_mode or not self.connection:
            return
            
        cursor = self.connection.cursor()
        
        # Agent communication table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agent_data (
                id VARCHAR(255) PRIMARY KEY,
                agent_id VARCHAR(100) NOT NULL,
                data_type VARCHAR(100) NOT NULL,
                data JSON NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP NULL,
                INDEX idx_agent_type (agent_id, data_type),
                INDEX idx_timestamp (timestamp)
            )
        """)
        
        # Property analysis results from Agent #1
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS property_intelligence (
                property_id VARCHAR(255) PRIMARY KEY,
                agent_id VARCHAR(100) DEFAULT 'agent_1',
                address TEXT NOT NULL,
                price_analysis JSON,
                market_comparison JSON,
                property_features JSON,
                investment_metrics JSON,
                risk_assessment JSON,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_address (address(100))
            )
        """)
        
        # Regional statistics from Agent #2
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS neighborhood_intelligence (
                region_id VARCHAR(255) PRIMARY KEY,
                agent_id VARCHAR(100) DEFAULT 'agent_2',
                region_name VARCHAR(255) NOT NULL,
                demographics JSON,
                amenities_analysis JSON,
                transport_scores JSON,
                safety_metrics JSON,
                lifestyle_fit JSON,
                market_trends JSON,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_region (region_name)
            )
        """)
        
        cursor.close()
        self.logger.info("✅ TiDB tables created/verified")
    
    def store_agent_data(self, agent_id: str, data_type: str, data: Dict, expires_hours: int = 24) -> bool:
        """Store data from an agent for other agents to consume"""
        if self.mock_mode:
            self.logger.info(f"[MOCK] Stored {data_type} from {agent_id}")
            return True
        
        try:
            cursor = self.connection.cursor()
            
            data_id = f"{agent_id}_{data_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            expires_at = datetime.now() + timedelta(hours=expires_hours)
            
            cursor.execute("""
                INSERT INTO agent_data (id, agent_id, data_type, data, expires_at)
                VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                data = VALUES(data), timestamp = CURRENT_TIMESTAMP
            """, (data_id, agent_id, data_type, json.dumps(data), expires_at))
            
            cursor.close()
            self.logger.info(f"✅ Stored {data_type} from {agent_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to store agent data: {e}")
            return False
    
    def get_agent_data(self, agent_id: str, data_type: str = None, limit: int = 100) -> List[Dict]:
        """Retrieve data from another agent"""
        if self.mock_mode:
            return self._get_mock_agent_data(agent_id, data_type)
        
        try:
            cursor = self.connection.cursor(pymysql.cursors.DictCursor)
            
            if data_type:
                cursor.execute("""
                    SELECT * FROM agent_data 
                    WHERE agent_id = %s AND data_type = %s 
                    AND (expires_at IS NULL OR expires_at > NOW())
                    ORDER BY timestamp DESC 
                    LIMIT %s
                """, (agent_id, data_type, limit))
            else:
                cursor.execute("""
                    SELECT * FROM agent_data 
                    WHERE agent_id = %s 
                    AND (expires_at IS NULL OR expires_at > NOW())
                    ORDER BY timestamp DESC 
                    LIMIT %s
                """, (agent_id, limit))
            
            results = cursor.fetchall()
            cursor.close()
            
            # Parse JSON data
            for result in results:
                result['data'] = json.loads(result['data'])
            
            self.logger.info(f"✅ Retrieved {len(results)} records from {agent_id}")
            return results
            
        except Exception as e:
            self.logger.error(f"❌ Failed to get agent data: {e}")
            return []
    
    def get_properties_from_agent1(self, location: str = "Austin, TX", limit: int = 20) -> List[Dict]:
        """Get property analysis from Agent #1 (Property Intelligence)"""
        if self.mock_mode:
            return self._get_mock_properties(location, limit)
        
        try:
            cursor = self.connection.cursor(pymysql.cursors.DictCursor)
            
            cursor.execute("""
                SELECT * FROM property_intelligence 
                WHERE address LIKE %s 
                ORDER BY timestamp DESC 
                LIMIT %s
            """, (f"%{location}%", limit))
            
            results = cursor.fetchall()
            cursor.close()
            
            # Parse JSON fields
            for result in results:
                result['price_analysis'] = json.loads(result['price_analysis'])
                result['market_comparison'] = json.loads(result['market_comparison'])
                result['property_features'] = json.loads(result['property_features'])
                result['investment_metrics'] = json.loads(result['investment_metrics'])
                result['risk_assessment'] = json.loads(result['risk_assessment'])
            
            self.logger.info(f"✅ Retrieved {len(results)} properties from Agent #1")
            return results
            
        except Exception as e:
            self.logger.error(f"❌ Failed to get properties from Agent #1: {e}")
            return self._get_mock_properties(location, limit)
    
    def get_regional_stats_from_agent2(self, region: str = "Austin, TX") -> Dict:
        """Get regional analysis from Agent #2 (Neighborhood Intelligence)"""
        if self.mock_mode:
            return self._get_mock_regional_stats(region)
        
        try:
            cursor = self.connection.cursor(pymysql.cursors.DictCursor)
            
            cursor.execute("""
                SELECT * FROM neighborhood_intelligence 
                WHERE region_name LIKE %s 
                ORDER BY timestamp DESC 
                LIMIT 1
            """, (f"%{region}%",))
            
            result = cursor.fetchone()
            cursor.close()
            
            if result:
                # Parse JSON fields
                result['demographics'] = json.loads(result['demographics'])
                result['amenities_analysis'] = json.loads(result['amenities_analysis'])
                result['transport_scores'] = json.loads(result['transport_scores'])
                result['safety_metrics'] = json.loads(result['safety_metrics'])
                result['lifestyle_fit'] = json.loads(result['lifestyle_fit'])
                result['market_trends'] = json.loads(result['market_trends'])
                
                self.logger.info(f"✅ Retrieved regional stats for {region} from Agent #2")
                return result
            else:
                self.logger.warning(f"No regional data found for {region}")
                return self._get_mock_regional_stats(region)
                
        except Exception as e:
            self.logger.error(f"❌ Failed to get regional stats from Agent #2: {e}")
            return self._get_mock_regional_stats(region)
    
    def _get_mock_agent_data(self, agent_id: str, data_type: str) -> List[Dict]:
        """Mock data for testing without TiDB"""
        mock_data = {
            'agent_1': {
                'property_analysis': [
                    {
                        'id': 'mock_1',
                        'agent_id': 'agent_1',
                        'data_type': 'property_analysis',
                        'data': {
                            'properties': [
                                {
                                    'address': '2505 San Gabriel St, Austin, TX 78705',
                                    'price': '$2,800/month',
                                    'analysis_score': 8.5,
                                    'market_position': 'competitive'
                                }
                            ]
                        },
                        'timestamp': datetime.now().isoformat()
                    }
                ]
            },
            'agent_2': {
                'regional_stats': [
                    {
                        'id': 'mock_2',
                        'agent_id': 'agent_2', 
                        'data_type': 'regional_stats',
                        'data': {
                            'region': 'Austin, TX',
                            'walkability_score': 7.2,
                            'safety_rating': 8.1,
                            'amenity_density': 'high'
                        },
                        'timestamp': datetime.now().isoformat()
                    }
                ]
            }
        }
        
        return mock_data.get(agent_id, {}).get(data_type, [])
    
    def _get_mock_properties(self, location: str, limit: int) -> List[Dict]:
        """Mock property data for testing"""
        return [
            {
                'property_id': 'mock_prop_001',
                'name': 'The Independent',
                'address': '2505 San Gabriel St, Austin, TX 78705',
                'price': '$2,800/month',
                'agent_name': 'Sarah Martinez',
                'agent_contact': {
                    'phone': '+15127891234',
                    'email': 'sarah.martinez@theindependent.com'
                },
                'price_analysis': {
                    'monthly_rent': 2800,
                    'price_per_sqft': 3.2,
                    'market_position': 'competitive',
                    'affordability_score': 7.5
                },
                'market_comparison': {
                    'comparable_avg': 2750,
                    'percentile_rank': 65,
                    'trend': 'stable'
                },
                'property_features': {
                    'bedrooms': 2,
                    'bathrooms': 2,
                    'sqft': 875,
                    'amenities': ['pool', 'gym', 'study_rooms'],
                    'pet_friendly': True
                },
                'investment_metrics': {
                    'roi_projection': 6.2,
                    'appreciation_potential': 'moderate',
                    'rental_demand': 'high'
                },
                'risk_assessment': {
                    'overall_risk': 'low',
                    'market_volatility': 'low',
                    'location_stability': 'high'
                },
                'timestamp': datetime.now().isoformat()
            },
            {
                'property_id': 'mock_prop_002',
                'name': 'East Austin Loft',
                'address': '2400 E 6th St, Austin, TX 78702',
                'price': '$2,600/month',
                'agent_name': 'Michael Chen',
                'agent_contact': {
                    'phone': '+15125551987',
                    'email': 'michael.chen@eastaustinloft.com'
                },
                'price_analysis': {
                    'monthly_rent': 2600,
                    'price_per_sqft': 2.9,
                    'market_position': 'value',
                    'affordability_score': 8.2
                },
                'market_comparison': {
                    'comparable_avg': 2650,
                    'percentile_rank': 48,
                    'trend': 'rising'
                },
                'property_features': {
                    'bedrooms': 2,
                    'bathrooms': 1,
                    'sqft': 900,
                    'amenities': ['pet_friendly', 'parking', 'rooftop_deck'],
                    'pet_friendly': True
                },
                'investment_metrics': {
                    'roi_projection': 7.1,
                    'appreciation_potential': 'high',
                    'rental_demand': 'very_high'
                },
                'risk_assessment': {
                    'overall_risk': 'low',
                    'market_volatility': 'moderate',
                    'location_stability': 'high'
                },
                'timestamp': datetime.now().isoformat()
            },
            {
                'property_id': 'mock_prop_003',
                'name': 'South Lamar Modern',
                'address': '1900 S Lamar Blvd, Austin, TX 78704',
                'price': '$3,200/month',
                'agent_name': 'Jessica Williams',
                'agent_contact': {
                    'phone': '+15124567890',
                    'email': 'j.williams@southlamarmodern.com'
                },
                'price_analysis': {
                    'monthly_rent': 3200,
                    'price_per_sqft': 3.5,
                    'market_position': 'premium',
                    'affordability_score': 6.8
                },
                'market_comparison': {
                    'comparable_avg': 3150,
                    'percentile_rank': 78,
                    'trend': 'rising'
                },
                'property_features': {
                    'bedrooms': 2,
                    'bathrooms': 2,
                    'sqft': 920,
                    'amenities': ['pool', 'gym', 'concierge', 'rooftop_lounge'],
                    'pet_friendly': True
                },
                'investment_metrics': {
                    'roi_projection': 5.8,
                    'appreciation_potential': 'high',
                    'rental_demand': 'high'
                },
                'risk_assessment': {
                    'overall_risk': 'low',
                    'market_volatility': 'low',
                    'location_stability': 'very_high'
                },
                'timestamp': datetime.now().isoformat()
            }
        ]
    
    def _get_mock_regional_stats(self, region: str) -> Dict:
        """Mock regional statistics for testing"""
        return {
            'region_id': f"mock_{region.lower().replace(', ', '_').replace(' ', '_')}",
            'region_name': region,
            'demographics': {
                'median_age': 28.5,
                'median_income': 75000,
                'education_level': 'high',
                'population_growth': 0.035
            },
            'amenities_analysis': {
                'restaurants_score': 8.7,
                'shopping_score': 7.4,
                'entertainment_score': 9.1,
                'parks_recreation': 7.9
            },
            'transport_scores': {
                'walkability': 72,
                'bike_score': 68,
                'transit_score': 41,
                'commute_time_avg': 24
            },
            'safety_metrics': {
                'crime_rate_index': 0.42,  # Lower is better
                'safety_score': 8.1,
                'emergency_response': 'excellent'
            },
            'lifestyle_fit': {
                'young_professional': 9.2,
                'family_friendly': 6.8,
                'student_oriented': 8.9,
                'retiree_suitable': 4.1
            },
            'market_trends': {
                'rental_growth_yoy': 0.042,
                'occupancy_rate': 0.94,
                'inventory_level': 'tight',
                'demand_forecast': 'growing'
            },
            'timestamp': datetime.now().isoformat()
        }
    
    def cleanup_expired_data(self):
        """Clean up expired data from shared memory"""
        if self.mock_mode:
            return
        
        try:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM agent_data WHERE expires_at IS NOT NULL AND expires_at < NOW()")
            deleted_count = cursor.rowcount
            cursor.close()
            
            self.logger.info(f"✅ Cleaned up {deleted_count} expired records")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to cleanup expired data: {e}")
    
    def close(self):
        """Close TiDB connection"""
        if self.connection:
            self.connection.close()
            self.logger.info("✅ TiDB connection closed")