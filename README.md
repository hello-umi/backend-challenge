# Landbot Backend Challenge

## Description

The product department wants a system to be notified when a customer requests assistance from a bot. The bot will make an http call (like a webhook) with the following information:

- Topic: a string with values can be sales or pricing
- Description: a string with a description of the problem that needs assistance from.

You need to expose an API endpoint that will receive this call and depending on the selected topic will forward it to a different channel:

``` 
Topic    | Channel   
----------------------
Sales    | Slack
Pricing  | Email
```
-----------------------------------------------------------------------
# SOLUTION TO THE CHALLENGE

## Architecture and tools
The project is structured as a Django app, using the Django Rest Framework for the speed-up in development of simple APIs.
As DDBB system I like postgres the most since it's the most reliable database in market, with multiple options for clustering and replication.
The asynchronous tasks are in charge of Celery + Redis, due to its good integration and simplicity. They also can scale horizontally as needed.
I also included a mailhog instance to mock the email server and prove that the integration works.


## Models

The main models for this app are Message and Topic. These models are essentially the data representation of the requested information.
Messages persist in DB with timestamps for creation and last edition, also with a status flag. This information could be used in the future to 
fine-tune and gain insights on the metrics and performance (more about that later)

Topics are just a list of defined topics, with the channel field as the strategy method to use.
Only topics with valid channels can be created by the API.


## Channels Strategy
Currently, only 2 channel integrations are implemented, but can be easily extended.
The `proxy.strategies.strategy_registry.py` file exposes a dict with the channel name as the key, 
and the actual class associated with it as value.
This class must be a subclass of the `MessagingStrategy`, that acts as a common interface.

How to extend the Channels available? Just create a new key in the dictionary and set the new `MessagingStrategy` 
subclass as its value.


## Workflow
The workflow is pretty straightforward:
1. When the app starts:
   1. Automatically creates the database and runs the migrations (if needed).
   2. The migrations include the already defined topics (in the problem description)
2. The API server listens to new calls to the /messages/ endpoints
3. When a valid POST request hits the server, the message is created with status 1-PENDING.
4. Just after the creation, the message is enqueued in Redis as a delayed task, and set the status 2-QUEUED
5. The latency for this operation is almost only network related.
6. The Celery Worker container takes the delayed task and delegates the message sending to the correct handler.
7. If the task is successfully executed, the status 4-SENT. Otherwise, the task is marked with status 3-ERROR
    

## Quickstart
To run the project just run `docker-compose up`.


## Docs

To read the API documentation you can just run the app and visit  `/swagger/` endpoint.

## Additional Notes
You will find some lack of "production ready" settings, such as DEBUG set to True and similar issues.
I assume that this is just a technical challenge, so you have the chance to test the candidates, but please take in mind 
the time-consuming effort that comes with it. I know some things *MUST* be changed.

## Out of scope

### Logging
As an improvement, the messages with errors could be stored in a new model that stores the exception messages, 
for further investigation of the root issues.
Also, since the messages not sent are flagged, it would be easy to retrieve them and send them again.

### Observability
Some kind of metrics could be exported to measure the performance of the app.
Other ideas could be indexing the messages into elasticsearch or other service similar, so we can trak anomalies.
Sure, integrations like Datadog or Sentry could be a huge improvement.

### Scalability
This one is easy, place a Load Balancer in front of the API server, and scale horizontally.
However, the bottleneck could be in the delayed tasks, so increasing the number of worker containers 
will improve substantially the overall performance.



-------------------------------------------
## Notes:
- Slack and Email are suggestions. Select one channel that you like the most, the other can be a mock.
- There may be more topics and channels in the future.

## The solution should:
- Be written in your favorite language and with the tools with which you feel comfortable.
- Be coded as you do daily (libraries, style, testing...).
- Be easy to grow with new functionality.
- Be a dockerized app.
