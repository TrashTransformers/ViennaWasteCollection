package org.waste.locator.model;

public class Coordinates {
    private final double x;
    private final double y;

    public Coordinates(double x, double y) {
        this.x = x;
        this.y = y;
    }

    public Coordinates(String coordinates) {
        coordinates = coordinates.replace("(", "");
        coordinates = coordinates.replace(")", "");
        String[] split = coordinates.contains(" ") ? coordinates.split(" ") : coordinates.split(",");
        x = Double.parseDouble(split[0]);
        y = Double.parseDouble(split[1]);
    }

    public double getX() {
        return x;
    }

    public double getY() {
        return y;
    }
}

