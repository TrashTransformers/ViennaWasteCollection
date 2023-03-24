package org.waste.locator.service;

import org.junit.jupiter.api.Test;
import org.waste.locator.csvreader.CollectionPointAltstoffCsvReader;
import org.waste.locator.csvreader.CollectionPointMistplatzCsvReader;
import org.waste.locator.csvreader.CollectionPointProblemstoffCsvReader;
import org.waste.locator.entity.CollectionPoint;
import org.waste.locator.model.Coordinates;

import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;

public class CsvReaderTest {
    public static final String FILENAME_ALTSTOFF = "ALTSTOFFSAMMLUNGOGD.csv";
    public static final String FILENAME_MISTPLATZ = "MISTPLATZOGD.csv";
    public static final String FILENAME_PROBLEMSTOFF = "PROBLEMSTOFFOGD.csv";

    @Test
    public void shouldReadFile() throws IOException {
        InputStream inputStream = getClass().getClassLoader().getResourceAsStream(FILENAME_ALTSTOFF);

        CollectionPointAltstoffCsvReader collectionPointAltstoffCsvReader = new CollectionPointAltstoffCsvReader();
        List<CollectionPoint> collectionPoints = collectionPointAltstoffCsvReader.readInput(inputStream);

        assertThat(collectionPoints).isNotEmpty();
        assertThat(collectionPoints).hasSize(4404);
    }

    @Test
    public void shouldReadFileMistplatz() {
        CollectionPointMistplatzCsvReader mistplatz = new CollectionPointMistplatzCsvReader();
        InputStream inputStream = getClass().getClassLoader().getResourceAsStream(FILENAME_MISTPLATZ);
        List<CollectionPoint> collectionPoints = mistplatz.readInput(inputStream, new ArrayList<>());

        assertThat(collectionPoints).isNotEmpty();
        assertThat(collectionPoints).hasSize(13);
    }

    @Test
    public void shouldReadFileProblemstoff() {
        CollectionPointProblemstoffCsvReader collectionPointAltstoffCsvReader = new CollectionPointProblemstoffCsvReader();
        InputStream inputStream = getClass().getClassLoader().getResourceAsStream(FILENAME_PROBLEMSTOFF);
        List<CollectionPoint> collectionPoints = collectionPointAltstoffCsvReader.readInput(inputStream, new ArrayList<>());

        assertThat(collectionPoints).isNotEmpty();
        assertThat(collectionPoints).hasSize(19);
    }

    @Test
    public void createCoordinates(){
        Coordinates coordinates = new Coordinates("10.00,12.54");
        assertThat(coordinates).isNotNull();
    }
}
