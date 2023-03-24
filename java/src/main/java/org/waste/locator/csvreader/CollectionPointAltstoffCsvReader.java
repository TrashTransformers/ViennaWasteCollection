package org.waste.locator.csvreader;

import org.waste.locator.entity.CollectionPoint;
import org.waste.locator.model.CollectionPointCategorie;
import org.waste.locator.model.Coordinates;

import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;

public class CollectionPointAltstoffCsvReader {

    public List<CollectionPoint> readInput(InputStream inputStream) {
        int lineNumber = 0;
        String line = "";
        List<CollectionPoint> collectionPoints = new ArrayList<>();
        try {
            BufferedReader br = new BufferedReader(new InputStreamReader(inputStream, StandardCharsets.UTF_8));
            while ((line = br.readLine()) != null) {

                if (lineNumber != 0) {
                    CollectionPoint collectionPoint = new CollectionPoint();
                    collectionPoints.add(collectionPoint);

                    String[] input = line.split(",");

                    String coordinates = input[1];
                    collectionPoint.setCoordinates(createCoordinates(coordinates));

                    String adresse = input[3] + " " + input[4] + " " + input[5] + "; " + input[2] + ". Bezirk";

                    collectionPoint.setAddress(adresse);

                    if (Integer.parseInt(input[8]) == 1) {
                        collectionPoint.addCollectionPointCategorie(CollectionPointCategorie.PAPER);
                    }
                    if (Integer.parseInt(input[9]) == 1) {
                        collectionPoint.addCollectionPointCategorie(CollectionPointCategorie.BIOMUELL);
                    }
                    if (Integer.parseInt(input[11]) == 1) {
                        collectionPoint.addCollectionPointCategorie(CollectionPointCategorie.GLASS);
                    }
                    if (Integer.parseInt(input[12]) == 1) {
                        collectionPoint.addCollectionPointCategorie(CollectionPointCategorie.PLASTIC);
                    }

                }
                lineNumber = +1;
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return collectionPoints;
    }

    private Coordinates createCoordinates(String coordinates) {
        String substring = coordinates.substring(7);
        String[] split = substring.split(" ");
        double yCoordinates = Double.parseDouble(split[0]);

        String[] split1 = split[1].split("\\)");
        double xCoordinates = Double.parseDouble(split1[0]);
        return new Coordinates(xCoordinates, yCoordinates);
    }

}
