# tud.addons.deepl - Automatic Translation Add-on for Plone

The `tud.addons.deepl` is a Plone add-on that leverages the DeepL API to provide automatic translations for texts in Plone websites.
This add-on aims to make it easier for Plone integrators to offer seamless and efficient translations to a wide range of different languages.
It integrates with the DeepL API to provide high-quality translations that can enhance the accessibility and reach of your Plone site's content.
For more details on the capabilities of the DeepL API please refer to the [DeepL API docs](https://www.deepl.com/en/docs-api/).

## Features

- Automatic Translation: The add-on seamlessly integrates with the DeepL API to provide automatic translations for your Plone content. This helps you quickly generate translations for your content without the need for manual intervention.

- Glossary Support: Utilizing the glossary feature of DeepL, this add-on allows you to add custom translations for specific words or phrases. This is particularly useful in domains with specialized lingo or terminology, ensuring accurate and consistent translations.

- Wide Language Support: DeepL supports translations for a wide variety of languages. With this add-on, you can offer translations to your users in multiple languages, thereby improving the user experience and making your content more accessible globally.

- Contributor's Flexibility: The tud.addons.deepl add-on provides contributors with the flexibility to implement meaningful integrations. Contributors can choose to create a user-interface for editors to initiate translations, develop utility scripts for translating content at specific intervals, or implement dynamic translation of pages on every page load. The add-on serves as a foundation for implementing the translation process according to your specific use case.

## Installation

1. Make sure you have a working instance of Plone version 4.3.19.

2. In your Plone instance, add `tud.addons.deepl` to your buildout configuration.

   ```ini
   [buildout]
   ...
   eggs =
       ...
       tud.addons.deepl
   ```

3. Run buildout to install the add-on.

   ```bash
   $ ./bin/buildout
   ```

4. Go to the Plone control panel and navigate to the Registry section.

5. Search for the `IDeepLAPISettings` entry.

6. Enter your DeepL API credentials (API key) in the provided fields.

7. Configure translation settings according to your preferences (e.g. glossary ID).

8. Save the settings.

## Usage

Once the add-on is installed and configured, it provides multiple endpoints:

### deepl_translate

This endpoint is used for translating a given text from a source language to a target language.

- Method: POST
- Header:
  - Accept: application/json
- Parameter (body, form-data)
  - text (required): text to be translated
  - source_language (optional, defaults to "en"): source language of the given text (e.g. "en", "de", "it")
  - target_language (optional, defaults to "de"): desired target language
- Permission required:
  - tud.addons.deepl: Request DeepL API (tud.addons.deepl.requestDeepLAPI)

A potential curl command would look this:

```bash
curl --location 'http://localhost:8080/Plone/deepl_translate' \
--header 'Accept: application/json' \
--form 'source_language="en"' \
--form 'target_language="de"' \
--form 'text="Hello, I am a sample sentence. Please translate me."'
```

The response is returned as JSON:

```json
{"status_code": 200, "result": "Hallo! Ich bin ein Beispielsatz. Bitte übersetze mich.", "error": null}
```

> **_NOTE:_**  The status code in the JSON is identical to the actual HTTP response code.

Please note that the accuracy and quality of translations may vary depending on the source content and the languages involved.
It's recommended to review and adjust translations as needed.

### deepl_usage

This endpoint gives you insight about the current character usage according to your selected plan for DeepL API.

- Method: GET
- Header:
  - Accept: application/json
- Permission required:
  - tud.addons.deepl: Request DeepL API (tud.addons.deepl.requestDeepLAPI)

A potential curl command would look this:

```bash
curl --location 'http://localhost:8080/Site/deepl_usage' \
--header 'Accept: application/json' \
```

The response is returned as JSON:

```json
{"status_code": 200, "result": {"character_count": 123, "character_limit": 500000}, "error": null}
```

> **_NOTE:_**  The status code in the JSON structure is identical to the actual HTTP response code.

## Permissions

Every endpoint can only be accessed via the permission "tud.addons.deepl: Request DeepL API".
By default this permission is granted to the Member role.
It can be granted to the Anonymous role (like done in the curl command), but note that this might attract unwanted API consumers.

## Testing

The `tud.addons.deepl` add-on includes a suite of tests to ensure its functionality and compatibility with Plone version 4.3.19.
To run the tests, follow these steps:

1. Activate the Plone testing environment.

   ```bash
   $ DEEPL_API_TOKEN=my-secret ./bin/instance test -s tud.addons.deepl
   ```

2. The tests will be executed, and the results will be displayed in the terminal.

## Dependencies to other add-ons:

- plone.rest
- plone.api

## Contributing

If you encounter any issues, have suggestions, or would like to contribute to the development of `tud.addons.deepl`, feel free to open an issue or submit a pull request on the [GitHub repository](https://github.com/tud-mit-plone/tud.addons.deepl).

## License

This add-on is released under the [MIT License](https://opensource.org/licenses/MIT).


