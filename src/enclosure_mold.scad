/**
 * @file enclosure_mold.scad
 * @brief Form-Molded Monolithic Interface Housing & Gasket Mold Core
 * @description Architecture for the Boeing/Lockheed Martin Bridge Node.
 * Conforms strictly to ACDelco-style flat-flange profiles. No snap-fits.
 */

// --- PARAMETER PARADIGMS (Adjustable Constants) ---
$fn = 64; // Surface smoothness resolution

// Enclosure Dimensions
casing_length = 240.0; 
casing_width  = 160.0;
casing_height = 80.0;
wall_thickness = 5.0;

// Flange & Mating Parameters (ACDelco Style Specification)
flange_width   = 18.0;
flange_thickness = 8.0;

// Gasket Compression Channel Parameters
gasket_width  = 4.5;
gasket_depth  = 3.0;

// Bolt Configuration Parameters
bolt_diameter = 6.5;   // Clearance for M6 fasteners
bolt_count_x  = 5;     // Number of bolts along length
bolt_count_y  = 4;     // Number of bolts along width


// --- RENDERING PIPELINE ---
// Toggle between rendering the bottom main enclosure housing or the top mating seal rim
render_bridge_node();


// --- CORE MODULES ---

module render_bridge_node() {
    difference() {
        // 1. Base Monolithic External Block with ACDelco Mating Flange
        union() {
            // Main Enclosure Body
            translate([0, 0, casing_height/2])
                cube([casing_length, casing_width, casing_height], center=true);
            
            // Continuous Perimeter Mating Flange (Strictly Molded - No Snaps)
            translate([0, 0, casing_height - flange_thickness/2])
                cube([casing_length + (flange_width * 2), casing_width + (flange_width * 2), flange_thickness], center=true);
        }
        
        // 2. Main Internal Electronic / Signal Cavity Isolation Space
        translate([0, 0, (casing_height / 2) + wall_thickness])
            cube([casing_length - (wall_thickness * 2), casing_width - (wall_thickness * 2), casing_height], center=true);
        
        // 3. Continuous Elastomeric Gasket Sealing Channel (Molded into Flange Face)
        translate([0, 0, casing_height - gasket_depth/2 + 0.01])
            gasket_path_subtraction();
        
        // 4. Form-Conformed Perimeter Bolt Array
        translate([0, 0, casing_height - flange_thickness - 0.5])
            bolt_pattern_array();
    }
}

module gasket_path_subtraction() {
    // Computes centerline coordinates for the continuous gasket routing path
    offset_x = (casing_length + flange_width) / 2;
    offset_y = (casing_width + flange_width) / 2;
    
    difference() {
        // Outer boundary of the gasket channel
        cube([offset_x * 2 + gasket_width, offset_y * 2 + gasket_width, gasket_depth + 0.1], center=true);
        // Inner boundary to form the continuous track wall
        cube([offset_x * 2 - gasket_width, offset_y * 2 - gasket_width, gasket_depth + 0.2], center=true);
    }
}

module bolt_pattern_array() {
    // Resolves placement boundary on the centerline of the extended flange rim
    pitch_x = (casing_length + flange_width) / (bolt_count_x - 1);
    pitch_y = (casing_width + flange_width) / (bolt_count_y - 1);
    
    start_x = -(casing_length + flange_width) / 2;
    start_y = -(casing_width + flange_width) / 2;
    
    // Cylindrical clearance punch holes for torque specification enforcement
    total_height = flange_thickness + 1.0;
    
    // X-Axis Arrays (Top and Bottom Flange Edges)
    for (i = [0 : bolt_count_x - 1]) {
        translate([start_x + (i * pitch_x), start_y, 0])
            cylinder(d=bolt_diameter, h=total_height, $fn=$fn);
            
        translate([start_x + (i * pitch_x), -start_y, 0])
            cylinder(d=bolt_diameter, h=total_height, $fn=$fn);
    }
    
    // Y-Axis Arrays (Left and Right Flange Edges - Excluding corner duplicates)
    for (j = [1 : bolt_count_y - 2]) {
        translate([start_x, start_y + (j * pitch_y), 0])
            cylinder(d=bolt_diameter, h=total_height, $fn=$fn);
            
        translate([-start_x, start_y + (j * pitch_y), 0])
            cylinder(d=bolt_diameter, h=total_height, $fn=$fn);
    }
}
