# fx_summarizer_api

This is a Restful API service that provide summarization service for any sort of content in English language. It utilizes basic Word Frequency algorithmn to determine which sentences are more important than the other. It is based on the assumption that the more repeated a word is, the more significance the statement may be. That said, stop words which are frequently used words but with no semantics, are not factored into consideration. 

Send a POST request to https://lzasummarizer.herokuapp.com/lza-projects/summaries and include a JSON in the HTTP body where the key is "content" and value is the content to be summarized. 

Example, sending a POST request with JSON looking like the following:
*{"content": "The US central bank announced a significant shift in its monetary policy stance to end 2021 ...}*

Example, responding result of a POST request. 
*{"summarized_content": "FOMC rate decision, the policy statement announced the accelerated pace of taper ($30 billion per month)... "}*
