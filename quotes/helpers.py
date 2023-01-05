from quotes.models import Quote
from quotes.quote_service import QuoteService
from states.models import State


def get_quote(quote_id: int) -> Quote:
    try:
        quote = Quote.objects.get(id=quote_id)
        return quote
    except Quote.DoesNotExist:
        return None


def update_quote(quote: Quote) -> Quote:
    state = State.objects.get(state=quote.state)
    if quote.updated_at < state.updated_at:
        QuoteService.update_existing_quote(quote, state)
        quote.refresh_from_db()
    return quote
