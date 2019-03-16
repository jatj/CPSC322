% file: untitled.pl

system(X).
hasSensor(X,laser).
hasSensor(X,window).
hasSensor(X,door).
live(X).
circuit_ok(c1).
circuit_ok(c2) <- circuit_ok(c1).
connected_to(laser,door) <- circuit_ok(c1).
connected_to(window,laser) <- circuit_ok(c2).
live(door) <- live(X).
live(laser) <- connected_to(laser,door) & live(door).
live(window) <- connected_to(window,laser) & live(laser).
triggered(X) <- door_open(X) & hasSensor(X,door) & live(door).
triggered(X) <- laser_interrupted(X) & hasSensor(X,laser) & live(laser).
triggered(X) <- window_broken(X) & hasSensor(X,window) & live(window).
alarm_triggered(X) <- triggered(X).

window_broken(X).
door_open(X).
laser_interrupted(X).
