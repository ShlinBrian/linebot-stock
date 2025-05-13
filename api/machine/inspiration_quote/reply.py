from common.line.classes import TextMessage
from common.line.utilities import reply_message
from config import Config
from loguru import logger
import openai, random


from ..classes import State

openai.api_key = Config.API_KEY

names = [
    "Steve Jobs",
    "Elon Musk",
    "Jeff Bezos",
    "Bill Gates",
    "Richard Branson",
    "Warren Buffett",
    "Mark Cuban",
    "Howard Schultz",
    "Oprah Winfrey",
    "Jack Ma",
    "Larry Page",
    "Sergey Brin",
    "Sundar Pichai",
    "Satya Nadella",
    "Tim Cook",
    "Reid Hoffman",
    "Sheryl Sandberg",
    "Sara Blakely",
    "Arianna Huffington",
    "Barbara Corcoran",
    "Rumi",
    "Pablo Neruda",
    "Kahlil Gibran",
    "Jane Austen",
    "William Shakespeare",
    "Emily Dickinson",
    "Elizabeth Barrett Browning",
    "John Keats",
    "Lord Byron",
    "Victor Hugo",
    "Erich Fromm",
    "Osho",
    "Maya Angelou",
    "Nicholas Sparks",
    "Leo Buscaglia",
    "Antoine de Saint-Exupéry",
    "Johann Wolfgang von Goethe",
    "Mark Twain",
    "Gabriel García Márquez",
    "Oscar Wilde",
    "Nelson Mandela",
    "Martin Luther King Jr.",
    "Mahatma Gandhi",
    "Dalai Lama",
    "Maya Angelou",
    "Eleanor Roosevelt",
    "Helen Keller",
    "Abraham Lincoln",
    "Theodore Roosevelt",
    "Anne Frank",
    "Desmond Tutu",
    "Malala Yousafzai",
    "Mother Teresa",
    "Franklin D. Roosevelt",
    "John F. Kennedy",
    "Steve Harvey",
    "Tony Robbins",
    "Brené Brown",
    "Simon Sinek",
    "James Clear",
    "Socrates",
    "Plato",
    "Aristotle",
    "Confucius",
    "Marcus Aurelius",
    "Epictetus",
    "Seneca",
    "Friedrich Nietzsche",
    "Immanuel Kant",
    "René Descartes",
    "Baruch Spinoza",
    "Søren Kierkegaard",
    "Michel de Montaigne",
    "David Hume",
    "Jean-Paul Sartre",
    "Albert Camus",
    "Simone de Beauvoir",
    "Hannah Arendt",
    "Ludwig Wittgenstein",
    "Slavoj Žižek",
    "Alan Watts",
    "Rainer Maria Rilke",
    "Carl Jung",
    "Viktor Frankl",
    "Hermann Hesse",
    "Ralph Waldo Emerson",
    "Henry David Thoreau",
    "Johann Wolfgang von Goethe",
    "Lao Tzu",
    "Sun Tzu",
    "Zhuang Zhou",
    "Voltaire",
    "Blaise Pascal",
    "Bertrand Russell",
    "Confucius",
    "Johann Gottlieb Fichte",
    "Mahavira",
    "Heraclitus",
    "Pythagoras",
    "Cicero",
]


class Reply(State):
    name = "reply"

    def execute(self, message="", **kwargs):
        response = self.analyze_message()

        reply_message(self.reply_token, [TextMessage(response)])

        return "OK"

    def analyze_message(self):
        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant that provides motivational and classic quotes.",
            },
            {
                "role": "user",
                "content": (
                    f"Give me a quote from {names[random.randint(0, len(names) - 1)]}."
                    "Please ensure that the response strictly adheres to a text format."
                ),
            },
        ]

        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=100,
            temperature=0.9,  # Balances creativity and relevance
            top_p=0.9,  # Promotes diverse output
        )
        result = response.choices[0].message.content
        logger.debug(f"messages: {messages}")
        logger.debug(f"result: {result}")
        return result
