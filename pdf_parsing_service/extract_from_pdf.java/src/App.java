import org.apache.tika.exception.TikaException;
import org.apache.tika.metadata.Metadata;
import org.apache.tika.parser.AutoDetectParser;
import org.apache.tika.sax.BodyContentHandler;
import org.apache.tika.parser.ParseContext;
import org.apache.tika.parser.Parser;
import org.xml.sax.ContentHandler;
import org.xml.sax.SAXException;
import org.apache.tika.metadata.Metadata;

import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.HashMap;
import java.util.Map;

public class App {

    public static Map<Integer, String> extractAndStoreSections(String pdfPath) throws IOException, SAXException, TikaException {
        Map<Integer, String> textBlocksMap = new HashMap<>();

        // Create a parser
        Parser parser = new AutoDetectParser();
        Metadata metadata = new Metadata();
        ContentHandler handler = new BodyContentHandler();

        // Parse the PDF
        try (InputStream stream = new FileInputStream(pdfPath)) {
            parser.parse(stream, handler, metadata, new ParseContext());
        }

        // Retrieve content as a single String
        String content = handler.toString();

        // Split the content into text blocks
        String[] textBlocks = content.split("\n\n");

        // Store each text block in the map
        for (int i = 0; i < textBlocks.length; i++) {
            textBlocksMap.put(i + 1, textBlocks[i].trim());
        }

        return textBlocksMap;
    }

    public static void main(String[] args) {
        try {
            Map<Integer, String> sections = extractAndStoreSections("C:\\Users\\H368246\\python_workspace\\hon-hackathon\\DocExtraction\\20221216105441_PURCHASE+ORDER+75450989.PDF");
            // Print sections or do something with them
            sections.forEach((key, value) -> System.out.println(key + ": " + value));
        } catch (IOException | SAXException e) {
            e.printStackTrace();
        }
    }

}
