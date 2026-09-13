/**
 * @file enclosure_mold.scad
 * @brief Form-Molded Bridge Node Enclosure Assembly with Internal Mounting Bosses
 * @description Driven by variable pipeline parameters. Employs flat-flange profiles.
 */

// --- DYNAMICALLY INJECTED OR PARAMETRIC VARIABLES ---
// (These fall back to default values if not explicitly rewritten by the pipeline script)
casing_length    = 240.0; 
casing_width     = 160.0;
casing_height    = 80.0;
wall_thickness   = 5.0;
flange_width     = 18.0;
flange_thickness = 8.0;
gasket_width     = 4.5;
gasket_depth     = 3.0;
bolt_diameter    = 6.5;   
bolt_count_x     = 5;     
bolt_count_y     = 4;     
boss_height      = 12.0;
boss_outer_dia   = 10.0;
boss_inner_dia   = 3.2;   // Sized for standard M3 self-tapping enclosure screws

$fn = 64; // High-fidelity circle resolution

// --- ASSEMBLY VIEW OR RENDERING SELECTION ---
// Change to "bottom", "top", or "assembly" for visualization/export
render_mode = "assembly"; 

if (render_mode == "bottom") {
    render_chassis_bottom();
} else if (render_mode == "top") {
    render_mating_lid();
} else if (render_mode == "assembly") {
    // Structural view showing both interlocking components split by a visibility gap
    render_chassis_bottom();
    translate([0, 0, casing_height + 40.0]) 
        rotate([180, 0, 0]) 
            render_mating_lid();
}


// --- CORE STRUCTURAL MODULES ---

module render_chassis_bottom() {
    difference() {
        union() {
            // Main Lower Body Block
            translate([0, 0, casing_height/2])
                cube([casing_length, casing_width, casing_height], center=true);
            
            // Continuous Perimeter Mating Flange (ACDelco Specification)
            translate([0, 0, casing_height - flange_thickness/2])
                cube([casing_length + (flange_width * 2), casing_width + (flange_width * 2), flange_thickness], center=true);
        }
        
        // Internal Electronic/Signal Cavity Isolation Space
        translate([0, 0, (casing_height / 2) + wall_thickness])
            cube([casing_length - (wall_thickness * 2), casing_width - (wall_thickness * 2), casing_height], center=true);
        
        // Continuous Elastomeric Gasket Sealing Recess
        translate([0, 0, casing_height - gasket_depth/2 + 0.01])
            gasket_path_subtraction();
        
        // Form-Conformed Perimeter Fastener Arrays
        translate([0, 0, casing_height - flange_thickness - 0.5])
            bolt_pattern_array();
    }
    
    // Add Internal Anchor Points to Bottom Floor
    internal_mounting_bosses();
}

module render_mating_lid() {
    lid_height = casing_height * 0.4; // Low-profile complementary upper lid casing
    
    difference() {
        union() {
            // Main Top Shell Block
            translate([0, 0, lid_height/2])
                cube([casing_length, casing_width, lid_height], center=true);
            
            // Mirror Mating Flange Rim
            translate([0, 0, lid_height - flange_thickness/2])
                cube([casing_length + (flange_width * 2), casing_width + (flange_width * 2), flange_thickness], center=true);
        }
        
        // Internal Lid Cavity Clearing Space
        translate([0, 0, (lid_height / 2) + wall_thickness])
            cube([casing_length - (wall_thickness * 2), casing_width - (wall_thickness * 2), lid_height], center=true);
        
        // Matching Transferred Bolt Pattern
        translate([0, 0, lid_height - flange_thickness - 0.5])
            bolt_pattern_array();
            
        // NOTE: The lid omits the gasket pocket subtraction channel. 
        // Its flat-molded face compresses perfectly flush against the bottom elastomer loop.
    }
}

module internal_mounting_bosses() {
    // Position boundaries relative to inner wall constraints
    span_x = (casing_length - (wall_thickness * 2)) / 3;
    span_y = (casing_width - (wall_thickness * 2)) / 3;
    
    // Generates a 4-point internal standoff system for backplanes or components
    for (x = [-span_x, span_x]) {
        for (y = [-span_y, span_y]) {
            translate([x, y, wall_thickness]) {
                difference() {
                    cylinder(d=boss_outer_dia, h=boss_height, $fn=$fn);
                    translate([0, 0, -0.1])
                        cylinder(d=boss_inner_dia, h=boss_height + 0.2, $fn=$fn);
                }
            }
        }
    }
}

module gasket_path_subtraction() {
    offset_x = (casing_length + flange_width) / 2;
    offset_y = (casing_width + flange_width) / 2;
    difference() {
        cube([offset_x * 2 + gasket_width, offset_y * 2 + gasket_width, gasket_depth + 0.1], center=true);
        cube([offset_x * 2 - gasket_width, offset_y * 2 - gasket_width, gasket_depth + 0.2], center=true);
    }
}

module bolt_pattern_array() {
    pitch_x = (casing_length + flange_width) / (bolt_count_x - 1);
    pitch_y = (casing_width + flange_width) / (bolt_count_y - 1);
    start_x = -(casing_length + flange_width) / 2;
    start_y = -(casing_width + flange_width) / 2;
    total_height = flange_thickness + 1.0;
    
    for (i = [0 : bolt_count_x - 1]) {
        translate([start_x + (i * pitch_x), start_y, 0]) cylinder(d=bolt_diameter, h=total_height, $fn=$fn);
        translate([start_x + (i * pitch_x), -start_y, 0]) cylinder(d=bolt_diameter, h=total_height, $fn=$fn);
    }
    for (j = [1 : bolt_count_y - 2]) {
        translate([start_x, start_y + (j * pitch_y), 0]) cylinder(d=bolt_diameter, h=total_height, $fn=$fn);
        translate([-start_x, start_y + (j * pitch_y), 0]) cylinder(d=bolt_diameter, h=total_height, $fn=$fn);
    }
}
