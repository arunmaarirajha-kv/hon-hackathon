import org.apache.tika.exception.TikaException;
import org.apache.tika.metadata.Metadata;
import org.apache.tika.parser.ParseContext;
import org.apache.tika.parser.pdf.PDFParser;
import org.apache.tika.sax.BodyContentHandler;
import org.xml.sax.SAXException;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;

public class App {
    public static void main(String[] args) {
        // Path to the PDF file
        String pdfFilePath = "20221216105441_PURCHASE+ORDER+75450989.PDF";

        // Create a content handler
        BodyContentHandler handler = new BodyContentHandler(); // -1 for no limit on the text extraction

        // Create metadata and parse context instances
        Metadata metadata = new Metadata();
        ParseContext pContext = new ParseContext();

        // PDF Parser
        PDFParser pdfParser = new PDFParser();

        try (FileInputStream inputStream = new FileInputStream(new File(pdfFilePath))) {
            // Parsing the document
            pdfParser.parse(inputStream, handler, metadata, pContext);
            // Extracted content as a string
            String extractedContent = handler.toString();
            System.out.println("Extracted Content: \n" + extractedContent);
        } catch (IOException | TikaException | SAXException e) {
            e.printStackTrace();
        }
    }
}

