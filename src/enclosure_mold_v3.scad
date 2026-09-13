/**
 * @file enclosure_mold.scad
 * @brief Dynamic Form-Molded Enclosure Core
 * @description Supports runtime-injected variable coordinate arrays for internal mounting.
 */

// --- BASE CASING PARAMETERS ---
casing_length    = 240.0; casing_width = 160.0; casing_height = 80.0; wall_thickness = 5.0;
flange_width     = 18.0; flange_thickness = 8.0; gasket_width = 4.5; gasket_depth = 3.0;
bolt_diameter    = 6.5; bolt_count_x = 5; bolt_count_y = 4;

// --- DYNAMIC STANDOFF ARRAY MATRIX ---
// Format: [ [X_pos, Y_pos, Inner_Dia, Outer_Dia, Height], ... ]
standoff_matrix = [
    [-60.0, -40.0, 3.2, 10.0, 12.0],
    [60.0, -40.0, 3.2, 10.0, 12.0],
    [60.0, 40.0, 3.2, 10.0, 12.0],
    [-60.0, 40.0, 3.2, 10.0, 12.0],
    [0.0, 0.0, 4.2, 12.0, 15.0]
];

$fn = 64;
render_mode = "bottom"; 

if (render_mode == "bottom") render_chassis_bottom();

module render_chassis_bottom() {
    difference() {
        union() {
            translate([0, 0, casing_height/2]) cube([casing_length, casing_width, casing_height], center=true);
            translate([0, 0, casing_height - flange_thickness/2]) cube([casing_length + (flange_width * 2), casing_width + (flange_width * 2), flange_thickness], center=true);
        }
        translate([0, 0, (casing_height / 2) + wall_thickness]) cube([casing_length - (wall_thickness * 2), casing_width - (wall_thickness * 2), casing_height], center=true);
        translate([0, 0, casing_height - gasket_depth/2 + 0.01]) gasket_path_subtraction();
        translate([0, 0, casing_height - flange_thickness - 0.5]) bolt_pattern_array();
    }
    generate_dynamic_standoffs();
}

module generate_dynamic_standoffs() {
    for (i = [0 : len(standoff_matrix) - 1]) {
        pt = standoff_matrix[i];
        translate([pt[0], pt[1], wall_thickness]) {
            difference() {
                cylinder(d=pt[3], h=pt[4], $fn=$fn);
                translate([0, 0, -0.1]) cylinder(d=pt[2], h=pt[4] + 0.2, $fn=$fn);
            }
        }
    }
}

module gasket_path_subtraction() {
    offset_x = (casing_length + flange_width) / 2; offset_y = (casing_width + flange_width) / 2;
    difference() {
        cube([offset_x * 2 + gasket_width, offset_y * 2 + gasket_width, gasket_depth + 0.1], center=true);
        cube([offset_x * 2 - gasket_width, offset_y * 2 - gasket_width, gasket_depth + 0.2], center=true);
    }
}

module bolt_pattern_array() {
    pitch_x = (casing_length + flange_width) / (bolt_count_x - 1); pitch_y = (casing_width + flange_width) / (bolt_count_y - 1);
    start_x = -(casing_length + flange_width) / 2; start_y = -(casing_width + flange_width) / 2;
    for (i = [0 : bolt_count_x - 1]) {
        translate([start_x + (i * pitch_x), start_y, 0]) cylinder(d=bolt_diameter, h=flange_thickness + 1.0);
        translate([start_x + (i * pitch_x), -start_y, 0]) cylinder(d=bolt_diameter, h=flange_thickness + 1.0);
    }
    for (j = [1 : bolt_count_y - 2]) {
        translate([start_x, start_y + (j * pitch_y), 0]) cylinder(d=bolt_diameter, h=flange_thickness + 1.0);
        translate([-start_x, start_y + (j * pitch_y), 0]) cylinder(d=bolt_diameter, h=flange_thickness + 1.0);
    }
}
