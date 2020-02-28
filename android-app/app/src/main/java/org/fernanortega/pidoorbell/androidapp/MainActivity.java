package org.fernanortega.pidoorbell.androidapp;

import android.annotation.SuppressLint;
import android.os.Bundle;
import android.view.MotionEvent;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

public class MainActivity extends AppCompatActivity {

    String TOUCH_URL_PUSH = "http://192.168.1.200/open_door/push";
    String TOUCH_URL_RELEASE = "http://192.168.1.200/open_door/release";
    // Create an anonymous implementation of OnClickListener
    private View.OnTouchListener touchListener = new View.OnTouchListener() {
        @Override
        public boolean onTouch(View v, MotionEvent event) {
            if (event.getAction() == MotionEvent.ACTION_DOWN) {
                // Pressed
                System.out.println("Pushing button to open door");
                onTouchAction(TOUCH_URL_PUSH);
            } else if (event.getAction() == MotionEvent.ACTION_UP) {
                // Released
                System.out.println("Releasing button to open door");
                onTouchAction(TOUCH_URL_RELEASE);
            }
            return true;
        }
    };

    private void onTouchAction(String url) {
        final TextView textView = findViewById(R.id.response_open_door);

        // Instantiate the RequestQueue.
        RequestQueue queue = Volley.newRequestQueue(this);

        // Request a string response from the provided URL.
        StringRequest stringRequest = new StringRequest(Request.Method.POST, url,
                new Response.Listener<String>() {
                    @Override
                    public void onResponse(String response) {
                        // Display the first 500 characters of the response string.
                        String message = getApplicationContext().getString(
                                R.string.response_message, response);
                        textView.setText(message);
                    }
                }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                textView.setText("That didn't work!");
            }
        });
        // Add the request to the RequestQueue.
        queue.add(stringRequest);
    }

    @SuppressLint("ClickableViewAccessibility")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Capture our button from layout
        Button button = findViewById(R.id.open_door);
        // Register the onClick listener with the implementation above
        button.setOnTouchListener(touchListener);

    }
}
