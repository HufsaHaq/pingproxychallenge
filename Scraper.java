import java.io.IOException;
import java.net.*;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.*;


public class Scraper{
    private static final int THREAD_COUNT = 10;
    private static final int TARGET = 25000;

    private static String runId = "";

    private static int minYear = 50000;
    private static int maxYear = 0;
    private static Map<String, Integer> makeDict = new HashMap<>();
    private static int total = 0;
    private static String mode = "";

    private static List<String> store = new ArrayList<>();

    private static final List<String> proxyPool = Arrays.asList(
        "http://pingproxies:scrapemequickly@194.87.135.1:9875",
        "http://pingproxies:scrapemequickly@194.87.135.2:9875",
        "http://pingproxies:scrapemequickly@194.87.135.3:9875",
        "http://pingproxies:scrapemequickly@194.87.135.4:9875",
        "http://pingproxies:scrapemequickly@194.87.135.5:9875"
    );

    
    public static void main(String[] args) throws Exception {
        runId = startScrapingRun("bace025d-120a-11f0-aaf0-0242ac120002");
        //submit(scraper(runId), runId);
    }

    public static String startScrapingRun(String args){
        HttpRequest request = HttpRequest.newBuilder()
        .uri(URI.create("https://api.scrapemequickly.com/scraping-run?team_id="+args))
        .method("POST", HttpRequest.BodyPublishers.noBody())
        .build();

        HttpResponse<String> response = null;
		try {
			response = HttpClient.newHttpClient().send(request, HttpResponse.BodyHandlers.ofString());
		} catch (IOException e) {
			e.printStackTrace();
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		System.out.println(response.body());
        return response.body();

    }


}

class GetData extends Thread{
    public String endpoint = "";
    public int index = 0;
    public String key = "";

    public GetData(String endpoint, int index, String key)
    {
        this.endpoint = endpoint;
        this.index = index;
        this.key = key;

    }
    @Override
    public void run()
    {
        
    }
}