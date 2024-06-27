PY = python3
NAME_AI = TTT_model.keras
SRC = main.py
LOG_DIR = logs

all:
	$(PY) $(SRC)

train: fclean
	$(PY) $(SRC)

stats:
	@if [ -d $(LOG_DIR) ]; then tensorboard --logdir $(LOG_DIR); fi

fclean:
	@if [ -d $(LOG_DIR) ]; then rm -rf $(LOG_DIR); fi
	@if [ -f $(NAME_AI) ]; then rm -rf $(NAME_AI); fi