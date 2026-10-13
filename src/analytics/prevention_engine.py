"""Preventive Measures, Root-Cause Analysis, and Hazard-to-Control Mapping Engine.
Synthesizes verified patterns, recurring failure modes, and safety controls grounded in DGMS data.
"""
import os
import sys
import json
from typing import List, Dict, Any

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

class PreventionEngine:
    def __init__(self, json_path: str = "data/extracted/inundation_incidents.json"):
        with open(json_path, "r", encoding="utf-8") as f:
            self.incidents = json.load(f)
            
    def get_hazard_control_matrix(self) -> List[Dict[str, Any]]:
        """Maps identified inundation hazards to direct cause, root cause, official controls, and AI engineering controls."""
        return [
            {
                "hazard_id": "HAZ-01",
                "hazard_title": "Puncturing of Waterlogged Old Workings",
                "category": "Underground Coal & Metal Mines",
                "frequency_severity": "High Catastrophic Severity (375 fatalities at Chasnalla, 63 at Newton Chikli, 29 at Bagdigi, 19 at Hurriladih)",
                "historical_evidence": [
                    "Chasnalla Colliery (1975) - 375 deaths [sanket_coal_2016_2022.pdf, p. 304]",
                    "Bagdigi Colliery (2001) - 29 deaths [sanket_coal_2016_2022.pdf, p. 305]",
                    "Newton Chikli (1954) - 63 deaths [sanket_coal_2016_2022.pdf, p. 303]",
                    "Hurriladih (1983) - 19 deaths [sanket_coal_2016_2022.pdf, p. 305]"
                ],
                "direct_cause": "Sudden violent rush of water and asphyxiating atmosphere into active workings upon piercing a thin coal barrier.",
                "established_root_cause": "Inaccurate or unverified historical mine boundary plans showing false protective barrier width; omission of advance exploratory burnside probe hole drilling before approaching within 60m of unchartered workings.",
                "potential_consequences": "Instantaneous flooding of lower levels, entrapment of entire underground shift, widespread loss of life, destruction of haulage and ventilation infrastructure.",
                "officially_recommended_controls": "Strict enforcement of Regulation 127/150 (60m statutory barrier zone); mandatory drilling of advance test boreholes fitted with burnside safety plugs; statutory survey correlation before commencing depillaring or development.",
                "ai_generated_preventive_suggestions": [
                    "Deploy modern 3D borehole radar and Electrical Resistivity Tomography (ERT) from inbye faces to detect water bodies through barriers up to 50m in advance.",
                    "Implement telemetry-enabled drilling rigs that automatically cease thrust and alarm when drill fluid pressure drops, indicating void intersection.",
                    "Establish refuge chambers equipped with independent compressed-air lifelines in dip districts located downhill from potential water sources."
                ],
                "monitoring_early_warning": "Continuous measurement of water seepage volume in advance probe holes; drill feed thrust and core return monitoring; hydrostatic pressure sensors installed in test holes.",
                "statutory_citations": "CMR Regulation 127(1)&(3), Regulation 129(1), CMR 2017 Regulation 150(2)&(3), DGMS Tech Circulars on Precaution Against Inundation.",
                "confidence_level": "High (1.0) - Grounded in multiple Courts of Inquiry."
            },
            {
                "hazard_id": "HAZ-02",
                "hazard_title": "Intervening Seam Parting Failure under Hydrostatic Head",
                "category": "Multi-Seam Underground Workings",
                "frequency_severity": "Fatal Trap Risk (2 deaths at Khoodia Colliery, 2020; also seen in Kuardih, 2017)",
                "historical_evidence": [
                    "Khoodia Colliery (08.12.2020) - 2 deaths [sanket_coal_2016_2022.pdf, p. 231]",
                    "Kuardih Colliery (25.07.2017) - 1 death [sanket_coal_2016_2022.pdf, p. 119]"
                ],
                "direct_cause": "Sudden shear failure and bursting of 4.5m thick rock parting separating active pumping station from waterlogged lower seam having higher hydrostatic head.",
                "established_root_cause": "Development within 60m of waterlogged seam without risk assessment under Regulation 150(2); geological disturbances and silty shale reducing parting shear strength; inaccurate geological plan failing to plot fault zones.",
                "potential_consequences": "Floor heave, violent water inrush from dip side, drowning of pumping crews, submerged electrical installations.",
                "officially_recommended_controls": "Prohibit development within 60m of waterlogged area in lower seam (CMR Reg 150(3)); maintain accurate plans showing dykes, faults, and boreholes (CMR Reg 65); comprehensive risk assessment before placing pumping stations below water level.",
                "ai_generated_preventive_suggestions": [
                    "Perform coupled hydro-mechanical geotechnical finite-element numerical modeling to calculate factor of safety across intervening partings subject to variable hydrostatic head.",
                    "Install vibrating wire piezometers across inter-seam partings to continuously track pore water pressure and hydraulic gradient.",
                    "Position all primary dewatering pumps on high-elevation drift niches with remote automated float controls to eliminate worker exposure in low dip sumps."
                ],
                "monitoring_early_warning": "Floor crack acoustic monitoring; piezometric pressure transducers; visual inspection for silty floor heave or sweating rock faces.",
                "statutory_citations": "CMR 2017 Regulation 150(2)(ii), Regulation 150(3), Regulation 65(1)(b), Regulation 104(1).",
                "confidence_level": "High (1.0) - Confirmed by DGMS Fatal Accident Summary No. 43 of 2020."
            },
            {
                "hazard_id": "HAZ-03",
                "hazard_title": "Surface River / Jore / Flood Ingress into Underground Mine",
                "category": "Surface-to-Underground Interconnection",
                "frequency_severity": "Catastrophic Disaster Risk (64 deaths at Gaslitand, 1 death at Kuardih)",
                "historical_evidence": [
                    "Gaslitand Colliery (27.09.1995) - 64 deaths [sanket_coal_2016_2022.pdf, p. 305]",
                    "Kuardih Colliery (25.07.2017) - 1 death [sanket_coal_2016_2022.pdf, p. 119]"
                ],
                "direct_cause": "River or jore overflowing banks, breaching embankments, or collapsing shallow subsided ground, flooding mine inclines and shaft mouths.",
                "established_root_cause": "Failure to withdraw miners when surface river crossed statutory danger level; presence of backfilled/abandoned pits and shallow subsidence fissures near watercourse; sub-standard flood embankments.",
                "potential_consequences": "Complete drowning of entire underground workings, destruction of fans and hoisting, catastrophic loss of life.",
                "officially_recommended_controls": "Strict adherence to HFL (Highest Flood Level) and HFL markings; mandatory withdrawal of all persons from underground when surface water reaches danger level; sealing and packing all subsidence potholes within leasehold.",
                "ai_generated_preventive_suggestions": [
                    "Implement IoT-connected ultrasonic water-level sensors on all adjacent rivers/jores linked via GSM/optical fiber to automatic audible alarm sirens and shaft gate interlocks.",
                    "Conduct seasonal high-resolution LiDAR drone topographic surveys before every monsoon to map new subsidence fractures and illegal mining sinkholes.",
                    "Design substantial concrete flood diversion canals and bunds engineered to withstand 100-year return flood peaks."
                ],
                "monitoring_early_warning": "Upstream river gauge monitoring; telemetry-linked rainfall alarms; pre-monsoon outcrop fissure inspections.",
                "statutory_citations": "CMR Regulation 126 (danger from surface water), Regulation 127, Regulation 150.",
                "confidence_level": "High (1.0) - Established by Court of Inquiry (Justice S.K. Mukherjee) and 2017 DGMS enquiry."
            },
            {
                "hazard_id": "HAZ-04",
                "hazard_title": "Failure of Underground Water Dam or Isolation Stopping",
                "category": "Underground Bulkhead Structures",
                "frequency_severity": "High Fatality Risk (2 deaths at Sayal 'D', 2017)",
                "historical_evidence": [
                    "Sayal 'D' Colliery (16.08.2017) - 2 deaths [sanket_coal_2016_2022.pdf, p. 118-119]"
                ],
                "direct_cause": "Brick isolation stopping washed away under static water head, releasing flood surge that swept workers into sump.",
                "established_root_cause": "Converting temporary brick partition stopping into water storage barrier without engineering design for water head; failure to build approved concrete water dam under Regulation 129(1).",
                "potential_consequences": "Sudden violent wave surge carrying muck and debris down roadway; drowning of workers downstream.",
                "officially_recommended_controls": "All water dams must be constructed to approved standard design under Regulation 129(1) read with DGMS Circular No. 7 of 1976; calculate maximum water head before storing water; no workers within 60m of impoundment.",
                "ai_generated_preventive_suggestions": [
                    "Enforce strict prohibition against using ventilation or isolation stoppings as water retaining walls.",
                    "Mandate certified reinforced concrete arched bulkhead dams with pressure-tested rock keyed abutments.",
                    "Incorporate automatic bypass drainage pipes and overflow relief valves to prevent head accumulation exceeding dam rating."
                ],
                "monitoring_early_warning": "Pressure sensors behind dam face; visual checks for leakage, bowing, or mortar degradation.",
                "statutory_citations": "CMR Regulation 129(1), DGMS Circular No. 7 of 1976 (Technical), CMR Regulation 127.",
                "confidence_level": "High (1.0) - Confirmed by DGMS Fatal Accident Summary No. 54 of 2017."
            },
            {
                "hazard_id": "HAZ-05",
                "hazard_title": "Hydraulic Stowing Barricade Puncture / Slurry Inrush",
                "category": "Underground Stowing Panels",
                "frequency_severity": "Burial and Suffocation Risk (1 death at Kakatiya Khani No 1 & 1A, 2018)",
                "historical_evidence": [
                    "Kakatiya Khani No 1 & 1A Incline (26.12.2018) - 1 death [sanket_coal_2016_2022.pdf, p. 155-156]"
                ],
                "direct_cause": "Worker swept away and buried under rushing sand and water slurry when rise-side stowing barricade punctured.",
                "established_root_cause": "Barricade structural failure under slurry pressure; deploying workman alone in dip gallery directly in the potential drainage path of active stowing.",
                "potential_consequences": "Rapid sand and water influx burying workers, suffocating air currents, blocking haulage dip.",
                "officially_recommended_controls": "Rigid stowing barricade inspection before pumping; strict supervision by shift Sirdar and Overman; prohibiting solitary work in drainage galleries.",
                "ai_generated_preventive_suggestions": [
                    "Standardize double-layer geotextile barricades with steel mesh reinforcement.",
                    "Equip stowing pipes with automatic density and flow control shutoff valves that instantly trip slurry pumps upon abnormal pressure loss.",
                    "Prohibit any personnel from entering galleries downstream of active stowing panels during pumping cycles."
                ],
                "monitoring_early_warning": "Drainage clarity monitoring (turbid sand water indicates tearing fabric); slurry pressure sensors.",
                "statutory_citations": "CMR 2017 Regulation 41(a), Regulation 42(2), Regulation 47(2)(c), Regulation 129(1), Regulation 239.",
                "confidence_level": "High (1.0) - Confirmed by DGMS Fatal Accident Summary No. 46 of 2018."
            },
            {
                "hazard_id": "HAZ-06",
                "hazard_title": "Sinking Shaft Sludge / Mud Inrush into Decline",
                "category": "Underground Metal / Metalliferous Mines",
                "frequency_severity": "High Multi-Casualty Threat (3 deaths, 9 injured at Turamdih Uranium, 2016)",
                "historical_evidence": [
                    "Turamdih Uranium Project (28.05.2016) - 3 deaths, 9 injured [sanket_non_coal_2016_2022.pdf, p. 81]"
                ],
                "direct_cause": "Sudden flow of 212 m³ of sludge and water into decline trapping and submerging 12 workers.",
                "established_root_cause": "Removing jammed sludge from bottom of 15.4m high sludge column in shaft without preventive barriers or risk assessment; lack of SOP under MMR Regulation 128(1).",
                "potential_consequences": "Instantaneous flooding of decline, asphyxiation of workers, complete entrapment.",
                "officially_recommended_controls": "Proper provisions to prevent irruption of sludge and water from shaft to decline; risk assessment study for cleaning sludge in shaft; framing and enforcement of SOP under Regulation 128(1) read with DGMS Circular 13 of 2002.",
                "ai_generated_preventive_suggestions": [
                    "Install heavy-duty hydraulic slice gates at all shaft-to-decline junctions before deepening shafts.",
                    "Mandate top-down vacuum dewatering or chemical coagulant injection to stabilize hung-up sludge plugs before bottom access.",
                    "Conduct all hung-up clearing operations using remotely operated equipment without personnel inside the decline."
                ],
                "monitoring_early_warning": "Shaft water/sludge level ultrasonic gauges; acoustic sensors on shaft lining.",
                "statutory_citations": "MMR 1961 Regulation 128(1), DGMS Technical Circular No. 13 of 2002.",
                "confidence_level": "High (1.0) - Confirmed by DGMS Non-Coal Fatal Accident Summary No. 35 of 2016."
            },
            {
                "hazard_id": "HAZ-07",
                "hazard_title": "Displacement Surge (Tsunami) Wave in Waterlogged Quarry",
                "category": "Opencast Stone & Metal Mines",
                "frequency_severity": "Sweeping Surge Drowning (3 deaths at Purnadih Nawada Stone, 2019)",
                "historical_evidence": [
                    "Purnadih Nawada Stone Mine (09.11.2019) - 3 deaths [sanket_non_coal_2016_2022.pdf, p. 215]"
                ],
                "direct_cause": "Workers on lower quarry bench swept into deep waterlogged pit by a 5-6m high displacement wave triggered by a massive rockfall.",
                "established_root_cause": "Working under dangerous 35-40m unbenched vertical highwall in violation of prohibitory order under Section 22(3); sudden collapse of 55m x 18m x 20m rockmass into 15-18m deep water.",
                "potential_consequences": "High-velocity wave surge submerging entire quarry floor and sweeping all workers into deep water.",
                "officially_recommended_controls": "Strict adherence to Section 22(3) prohibitory orders; adequate benching under MMR Regulation 106(3); dewatering waterlogged quarries before deploying men at base.",
                "ai_generated_preventive_suggestions": [
                    "Mandate hydro-dynamic wave run-up simulations before allowing operations in quarries adjacent to deep water pools.",
                    "Dewater quarry pits before operating machines or men within the run-up zone.",
                    "Deploy real-time slope radar (SSR) on unstable highwalls overlooking standing water."
                ],
                "monitoring_early_warning": "Micro-seismic slope monitoring; tension crack displacement extensometers.",
                "statutory_citations": "Mines Act Section 22(3), MMR 1961 Regulation 106(3), Regulation 34(1).",
                "confidence_level": "High (1.0) - Confirmed by DGMS Non-Coal Fatal Accident Summary No. 45 of 2019."
            }
        ]

    def get_summary_statistics(self) -> Dict[str, Any]:
        """Calculates exact aggregate statistics from verified data."""
        verified = [inc for inc in self.incidents if inc.get("is_verified_inundation")]
        
        years = {}
        minerals = {}
        mine_types = {}
        sources = {}
        
        for inc in verified:
            yr = inc.get("accident_date", "")[:4]
            if yr.isdigit():
                years[yr] = years.get(yr, 0) + 1
                
            mineral_type = inc.get("mineral", "Unknown")
            minerals[mineral_type] = minerals.get(mineral_type, 0) + 1
            
            mt = inc.get("mine_type", "Unknown")
            mine_types[mt] = mine_types.get(mt, 0) + 1
            
            src = inc.get("inundation_source") or "Old Workings / Natural Water"
            sources[src] = sources.get(src, 0) + 1
            
        valid_yrs = [int(k) for k in years.keys() if k.isdigit()]
        return {
            "total_verified_incidents": len(verified),
            "total_verified_fatalities": sum(inc.get("fatalities", 0) for inc in verified),
            "total_verified_injuries": sum(inc.get("serious_injuries", 0) for inc in verified),
            "by_mineral": minerals,
            "by_mine_type": mine_types,
            "by_source": sources,
            "earliest_year": min(valid_yrs) if valid_yrs else 1901,
            "latest_year": max(valid_yrs) if valid_yrs else 2022
        }

if __name__ == "__main__":
    engine = PreventionEngine()
    stats = engine.get_summary_statistics()
    print("Prevention Engine initialized successfully.")
    print(f"Verified Inundations: {stats['total_verified_incidents']}, Fatalities: {stats['total_verified_fatalities']}")
    matrix = engine.get_hazard_control_matrix()
    print(f"Mapped {len(matrix)} Major Inundation Hazard Patterns.")
