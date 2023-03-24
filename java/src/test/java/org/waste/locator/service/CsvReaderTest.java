package org.waste.locator.service;

import org.junit.jupiter.api.Test;
import org.waste.locator.csvreader.CollectionPointAltstoffCsvReader;
import org.waste.locator.csvreader.CollectionPointMistplatzCsvReader;
import org.waste.locator.csvreader.CollectionPointProblemstoffCsvReader;
import org.waste.locator.entity.CollectionPoint;
import org.waste.locator.model.Coordinates;

import java.util.ArrayList;
import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;

public class CsvReaderTest {
    public static final String FILE_PATH_ALTSTOFF = "C:\\dev\\hackaton\\ViennaWastePointLocator\\Java\\src\\test\\resources\\ALTSTOFFSAMMLUNGOGD.csv";
    public static final String FILE_PATH_MISTPLATZ = "C:\\dev\\hackaton\\ViennaWastePointLocator\\Java\\src\\test\\resources\\MISTPLATZOGD.csv";
    public static final String FILE_PATH_PROBLEMSTOFF = "C:\\dev\\hackaton\\ViennaWastePointLocator\\Java\\src\\test\\resources\\PROBLEMSTOFFOGD.csv";

    @Test
    public void shouldReadFile() {
        CollectionPointAltstoffCsvReader collectionPointAltstoffCsvReader = new CollectionPointAltstoffCsvReader();
        List<CollectionPoint> collectionPoints = collectionPointAltstoffCsvReader.readInput(FILE_PATH_ALTSTOFF);

        assertThat(collectionPoints).isNotEmpty();
        assertThat(collectionPoints).hasSize(4404);
    }

    @Test
    public void shouldReadFileMistplatz() {
        CollectionPointMistplatzCsvReader mistplatz = new CollectionPointMistplatzCsvReader();
        List<CollectionPoint> collectionPoints = mistplatz.readInput(FILE_PATH_MISTPLATZ, new ArrayList<>());

        assertThat(collectionPoints).isNotEmpty();
        assertThat(collectionPoints).hasSize(13);
    }

    @Test
    public void shouldReadFileProblemstoff() {
        CollectionPointProblemstoffCsvReader collectionPointAltstoffCsvReader = new CollectionPointProblemstoffCsvReader();
        List<CollectionPoint> collectionPoints = collectionPointAltstoffCsvReader.readInput(FILE_PATH_PROBLEMSTOFF, new ArrayList<>());

        assertThat(collectionPoints).isNotEmpty();
        assertThat(collectionPoints).hasSize(19);
    }

    @Test
    public void createCoordinates(){
        Coordinates coordinates = new Coordinates("10.00,12.54");
        assertThat(coordinates).isNotNull();
    }
}
