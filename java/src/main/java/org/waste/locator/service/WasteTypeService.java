package org.waste.locator.service;

import org.gavaghan.geodesy.Ellipsoid;
import org.gavaghan.geodesy.GeodeticCalculator;
import org.gavaghan.geodesy.GlobalCoordinates;
import org.springframework.stereotype.Service;
import org.waste.locator.csvreader.CollectionPointAltstoffCsvReader;
import org.waste.locator.csvreader.CollectionPointMistplatzCsvReader;
import org.waste.locator.csvreader.CollectionPointProblemstoffCsvReader;
import org.waste.locator.entity.CollectionPoint;
import org.waste.locator.model.CollectionPointCategorie;
import org.waste.locator.model.Coordinates;

import java.util.ArrayList;
import java.util.List;

@Service
public class WasteTypeService {
    public static final String FILE_PATH_ALTSTOFF = "C:\\dev\\hackaton\\ViennaWastePointLocator\\Java\\src\\test\\resources\\ALTSTOFFSAMMLUNGOGD.csv";
    public static final String FILE_PATH_MISTPLATZ = "C:\\dev\\hackaton\\ViennaWastePointLocator\\Java\\src\\test\\resources\\MISTPLATZOGD.csv";
    public static final String FILE_PATH_PROBLEMSTOFF = "C:\\dev\\hackaton\\ViennaWastePointLocator\\Java\\src\\test\\resources\\PROBLEMSTOFFOGD.csv";


    private List<CollectionPoint> readCsvFiles(){
        CollectionPointAltstoffCsvReader altstoff = new CollectionPointAltstoffCsvReader();
        List<CollectionPoint> collectionPoints = altstoff.readInput(FILE_PATH_ALTSTOFF);

        CollectionPointMistplatzCsvReader mistplatz = new CollectionPointMistplatzCsvReader();
        mistplatz.readInput(FILE_PATH_MISTPLATZ, collectionPoints);

        CollectionPointProblemstoffCsvReader problemstoff = new CollectionPointProblemstoffCsvReader();
        problemstoff.readInput(FILE_PATH_PROBLEMSTOFF, collectionPoints);

        return collectionPoints;

    }

    public CollectionPoint calculateNearestCollectionPoint(String currentCoordinates, String disposalType) {
        CollectionPointCategorie wasteType = WasteMapper.getTypeFromInput(disposalType);

        List<CollectionPoint> collectionPoints = readCsvFiles();
        List<CollectionPoint> filteredList = new ArrayList<>();

        for (CollectionPoint collectionPoint : collectionPoints){
            List<CollectionPointCategorie> collectionPointCategorieList = collectionPoint.getCollectionPointCategorieList();
            if (collectionPointCategorieList.contains(wasteType)){
                filteredList.add(collectionPoint);
            }
        }
        return findClosestCoordinate(new Coordinates(currentCoordinates), filteredList);
    }

    public static CollectionPoint findClosestCoordinate(Coordinates point, List<CollectionPoint> coordinates) {
            Coordinates closestCoordinate = null;
            CollectionPoint closestCollection = null;
            double closestDistance = 0.0;

            for (CollectionPoint collectionPoint : coordinates){
                double distance = calculateDistance(point, collectionPoint.getCoordinate());
                if (closestCoordinate == null || distance < closestDistance) {
                    closestCoordinate = collectionPoint.getCoordinate();
                    closestDistance = distance;
                    closestCollection = collectionPoint;
                }
            }
            return closestCollection;
        }


        public static double calculateDistance(Coordinates point,Coordinates compare) {
            GlobalCoordinates point1 = new GlobalCoordinates(point.getX(), point.getY());
            GlobalCoordinates point2 = new GlobalCoordinates(compare.getX(), compare.getY());

            GeodeticCalculator calculator = new GeodeticCalculator();
            return calculator.calculateGeodeticCurve(Ellipsoid.WGS84, point1, point2).getEllipsoidalDistance();

        }
    }

